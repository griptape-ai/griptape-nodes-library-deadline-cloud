"""Tests for how a Deadline Cloud job's spend counts toward the run that submitted it.

The job templates define a `ParentRunId` parameter, and the worker script hands its value to the
workflow's executor. The submitting node names its own run in that parameter, but only when the job
template defines it: a template published before it existed doesn't, and Open Job Description refuses
a job that sets a parameter its template doesn't define.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock

import pytest
from griptape_nodes.exe_types.node_types import aprocess_scope
from griptape_nodes.retained_mode.events.budget_events import RunAttribution

from publish.deadline_cloud_job_template_generator import DeadlineCloudJobTemplateGenerator
from publish.deadline_cloud_multi_task_publisher import DeadlineCloudMultiTaskPublisher, MultiTaskPublisherConfig
from publish.deadline_cloud_multi_task_template_generator import DeadlineCloudMultiTaskJobTemplateGenerator
from publish.deadline_cloud_published_workflow import DeadlineCloudPublishedWorkflow
from publish.utils import PARENT_RUN_ID_PARAMETER, parent_run_id_job_parameters

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

# Starting the engine in a fresh process takes a few seconds; this leaves room for a slow CI runner.
WORKER_SCRIPT_TIMEOUT_SECONDS = 120


def _single_task_template(job_bundle_dir: Path) -> dict[str, Any]:
    return DeadlineCloudJobTemplateGenerator.generate_job_template(job_bundle_dir, "Parent", [])


def _multi_task_template(job_bundle_dir: Path) -> dict[str, Any]:
    return DeadlineCloudMultiTaskJobTemplateGenerator.generate_job_template(job_bundle_dir, "Parent", [], 1)


TEMPLATES = pytest.mark.parametrize(
    "generate_template", [_single_task_template, _multi_task_template], ids=["single task", "multi task"]
)


def _template_published_before_parent_run_ids(job_bundle_dir: Path) -> dict[str, Any]:
    template = _single_task_template(job_bundle_dir)
    template["parameterDefinitions"] = [
        definition for definition in template["parameterDefinitions"] if definition["name"] != PARENT_RUN_ID_PARAMETER
    ]
    return template


def test_a_template_that_defines_it_is_given_the_parent_run(tmp_path: Path) -> None:
    template = _single_task_template(tmp_path)

    assert parent_run_id_job_parameters(template, "run-1") == {PARENT_RUN_ID_PARAMETER: {"string": "run-1"}}


def test_a_template_published_before_it_existed_is_not_given_it(tmp_path: Path) -> None:
    """The job is submitted without the parameter, so Deadline Cloud doesn't refuse it."""
    template = _template_published_before_parent_run_ids(tmp_path)

    assert parent_run_id_job_parameters(template, "run-1") == {}


def test_no_run_names_no_parent(tmp_path: Path) -> None:
    template = _single_task_template(tmp_path)

    assert parent_run_id_job_parameters(template, None) == {}


def _run_published_node(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, job_template: dict[str, Any], run: RunAttribution | None
) -> dict[str, Any]:
    """Run the published-workflow node against stubbed AWS calls and return the job parameters it submitted."""
    node = DeadlineCloudPublishedWorkflow(
        name="Published Workflow",
        metadata={
            "job_template": job_template,
            "attachments": {"manifests": [{"rootPath": str(tmp_path)}]},
            "relative_dir_path": str(tmp_path),
            "models_dir_path": str(tmp_path / "models"),
            "workflow_shape": {},
        },
    )
    for name, value in {"farm_id": "farm-1", "queue_id": "queue-1"}.items():
        node.set_parameter_value(name, value)
    input_json_path = tmp_path / "inputs" / "input.json"
    submitted: list[dict[str, Any]] = []

    def submit_job(**kwargs: Any) -> str:
        submitted.append(kwargs["job_parameters"])
        return "job-1"

    monkeypatch.setattr(node, "_get_storage_profile_for_queue", lambda *_: None)
    monkeypatch.setattr(node, "_upload_attachments_to_s3", lambda *_: (str(input_json_path), {}))
    monkeypatch.setattr(node, "_combine_attachments", lambda *_: {})
    monkeypatch.setattr(node, "_submit_job_with_attachments", submit_job)
    monkeypatch.setattr(node, "_poll_job", lambda **_: None)
    monkeypatch.setattr(node, "_get_workflow_output", lambda **_: {})

    with aprocess_scope(node=node, run=run):
        node._process()

    assert len(submitted) == 1, node.get_parameter_value("result_details")
    return submitted[0]


def test_the_published_node_names_its_run_on_the_job(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    job_parameters = _run_published_node(
        monkeypatch, tmp_path, _single_task_template(tmp_path), RunAttribution(run_id="run-1")
    )

    assert job_parameters[PARENT_RUN_ID_PARAMETER] == {"string": "run-1"}


def test_the_published_node_leaves_it_off_an_older_template(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    job_parameters = _run_published_node(
        monkeypatch, tmp_path, _template_published_before_parent_run_ids(tmp_path), RunAttribution(run_id="run-1")
    )

    assert PARENT_RUN_ID_PARAMETER not in job_parameters


def test_the_multi_task_job_names_the_run_that_submitted_it(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    publisher = DeadlineCloudMultiTaskPublisher(
        MultiTaskPublisherConfig(
            workflow_name="Parent",
            parameter_values_per_iteration={0: {}},
            package_result=MagicMock(),
            farm_id="farm-1",
            queue_id="queue-1",
            parent_run_id="run-1",
        )
    )
    publisher._job_template = _multi_task_template(tmp_path)
    client = MagicMock()
    client.create_job.return_value = {"jobId": "job-1"}
    monkeypatch.setattr(publisher, "_get_client", lambda: client)
    monkeypatch.setattr(publisher, "_get_huggingface_cache_dir", lambda: str(tmp_path / "models"))

    publisher._submit_multi_task_job(str(tmp_path), MagicMock(manifests=[]))

    assert client.create_job.call_args.kwargs["parameters"][PARENT_RUN_ID_PARAMETER] == {"string": "run-1"}


def _substitute_job_parameters(script: str, values: dict[str, str]) -> str:
    """Fill in `{{Param.Name}}` the way Open Job Description does before the worker runs the script."""

    def value_for(match: re.Match[str]) -> str:
        return values[match.group(1)]

    return re.sub(r"\{\{Param\.(\w+)\}\}", value_for, script)


def _run_worker_script(
    tmp_path: Path, generate_template: Callable[[Path], dict[str, Any]], parent_run_id: str
) -> dict[str, Any]:
    """Run the job's worker script as Deadline Cloud would, and report what its executor was given.

    The script runs unchanged apart from the parameter values, in a process of its own, since it
    starts the engine at import. The job's `deadline_cloud_workflow_executor.py` and `workflow.py`,
    which publishing bundles, are replaced by ones that report the executor's arguments instead of
    running a flow.
    """
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    template = generate_template(bundle)
    script = template["steps"][0]["script"]["embeddedFiles"][0]["data"]
    location = tmp_path / "job"
    assets = location / "assets"
    assets.mkdir(parents=True)
    (assets / "deadline_cloud_workflow_executor.py").write_text(
        "class DeadlineCloudWorkflowExecutor:\n    def __init__(self, **kwargs):\n        self.kwargs = kwargs\n"
    )
    (assets / "workflow.py").write_text(
        "import json\n"
        "def execute_workflow(input, workflow_executor, pickle_control_flow_result):\n"
        "    print('EXECUTOR ' + json.dumps({'parent_run_id': workflow_executor.kwargs['parent_run_id']}))\n"
    )
    script_path = tmp_path / "run.py"
    script_path.write_text(
        _substitute_job_parameters(
            script,
            {
                "LocationToRemap": str(location),
                "ModelsLocationToRemap": str(tmp_path / "models"),
                "OutputDir": "out",
                PARENT_RUN_ID_PARAMETER: parent_run_id,
            },
        )
    )

    env = {key: value for key, value in os.environ.items() if not key.startswith("GTN_")}
    # Keep the engine's user config, data and logs, which starting it writes, out of the developer's own.
    env["XDG_CONFIG_HOME"] = str(tmp_path / "config")
    env["XDG_DATA_HOME"] = str(tmp_path / "data")
    env["XDG_STATE_HOME"] = str(tmp_path / "state")
    completed = subprocess.run(  # noqa: S603
        [sys.executable, str(script_path)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=WORKER_SCRIPT_TIMEOUT_SECONDS,
        check=False,
    )
    lines = [line for line in completed.stdout.splitlines() if line.startswith("EXECUTOR ")]
    assert len(lines) == 1, completed.stdout + completed.stderr
    return json.loads(lines[0].removeprefix("EXECUTOR "))


@TEMPLATES
def test_the_worker_hands_the_parent_run_to_its_executor(
    tmp_path: Path, generate_template: Callable[[Path], dict[str, Any]]
) -> None:
    executor = _run_worker_script(tmp_path, generate_template, "run-1")

    assert executor == {"parent_run_id": "run-1"}


@TEMPLATES
def test_the_worker_runs_without_a_parent_run(
    tmp_path: Path, generate_template: Callable[[Path], dict[str, Any]]
) -> None:
    """The parameter's empty default, for a job submitted with no run, reaches the executor as no parent."""
    executor = _run_worker_script(tmp_path, generate_template, "")

    assert executor == {"parent_run_id": None}


def test_the_template_names_no_parent_by_default(tmp_path: Path) -> None:
    """A job submitted without the parameter gets the empty default, which the worker reads as no parent."""
    definitions = {d["name"]: d for d in _single_task_template(tmp_path)["parameterDefinitions"]}

    assert definitions[PARENT_RUN_ID_PARAMETER]["default"] == ""


def test_the_multi_task_group_submits_its_job_under_the_run_in_progress(monkeypatch: pytest.MonkeyPatch) -> None:
    """The group's body runs without `run_attribution`, so it names the engine's run in progress instead.

    The group is built without its constructor, which needs the library registered with the engine,
    and everything `_arun` does before it configures the publisher is stubbed.
    """
    from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

    import publish.deadline_cloud_multi_task_publisher as publisher_module
    from execution.deadline_cloud_multi_task_group import DeadlineCloudMultiTaskGroup

    configs: list[MultiTaskPublisherConfig] = []

    class RecordingPublisher:
        def __init__(self, config: MultiTaskPublisherConfig) -> None:
            configs.append(config)

        async def publish_and_execute(self) -> list[Any]:
            return []

    async def package_group_body() -> Any:
        return MagicMock()

    group = DeadlineCloudMultiTaskGroup.__new__(DeadlineCloudMultiTaskGroup)
    group.name = "Group"
    monkeypatch.setattr(group, "parameter_output_values", {}, raising=False)
    monkeypatch.setattr(group, "_initialize_iteration_data", lambda: None)
    monkeypatch.setattr(group, "_get_total_iterations", lambda: 1)
    monkeypatch.setattr(group, "_package_group_body", package_group_body)
    monkeypatch.setattr(group, "_get_merged_parameter_values_for_iterations", lambda _: {0: {}})
    monkeypatch.setattr(group, "_get_result_parameter_name", lambda _: None)
    monkeypatch.setattr(group, "_get_start_flow_parameter_value", lambda _name, default=None: default)
    monkeypatch.setattr(group, "_build_host_requirements", lambda: None)
    monkeypatch.setattr(group, "get_all_nodes", dict)
    monkeypatch.setattr(publisher_module, "DeadlineCloudMultiTaskPublisher", RecordingPublisher)
    monkeypatch.setattr(GriptapeNodes, "FlowManager", lambda: MagicMock(spend_run_id="run-1"))

    asyncio.run(group._arun())

    assert [config.parent_run_id for config in configs] == ["run-1"]
