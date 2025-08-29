"""Job template generation for AWS Deadline Cloud workflows."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import yaml

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger("job_template_generator")


class DeadlineCloudJobTemplateGenerator:
    """Handles generation of Open Job Description templates for Griptape workflows."""

    @staticmethod
    def generate_job_template(job_bundle_dir: Path, workflow_name: str, library_paths: list[str]) -> dict[str, Any]:
        """Generate Open Job Description template for the workflow."""
        parameter_definitions: list[dict[str, Any]] = []

        parameter_definitions.append(
            {
                "name": "DataDir",
                "type": "PATH",
                "objectType": "DIRECTORY",
                "dataFlow": "INOUT",
                "description": "Directory containing job attachments and workflow files",
            }
        )

        parameter_definitions.append(
            {
                "name": "LocationToRemap",
                "type": "PATH",
                "description": "Top level directory to remap in the job attachments",
            }
        )

        parameter_definitions.append(
            {
                "name": "ModelsLocationToRemap",
                "type": "PATH",
                "description": "Directory path to remap HuggingFace model cache location",
            }
        )

        parameter_definitions.append(
            {
                "name": "InputFile",
                "type": "PATH",
                "objectType": "FILE",
                "dataFlow": "IN",
                "description": "Path to JSON file containing input for the workflow",
            }
        )

        # Generate Python execution script
        python_script = DeadlineCloudJobTemplateGenerator._generate_python_execution_script(library_paths)

        venv_script = """#!/bin/env bash
echo 'Setting up Python virtual environment...'
python -m pip install --upgrade pip wheel setuptools
echo 'Installing dependencies...'
pip install -r {{Param.LocationToRemap}}/assets/requirements.txt
mkdir -p {{Param.LocationToRemap}}/output
echo 'Virtual environment setup complete.'
"""

        # Create job template
        job_template: dict[str, Any] = {
            "specificationVersion": "jobtemplate-2023-09",
            "name": f"Griptape Workflow: {workflow_name}",
            "parameterDefinitions": parameter_definitions,
            "jobEnvironments": [
                {
                    "name": "Python312_Venv",
                    "description": "Python 3.12 virtual environment setup",
                    "script": {
                        "actions": {
                            "onEnter": {
                                "command": "bash",
                                "args": ["{{Env.File.Enter}}"],
                            }
                        },
                        "embeddedFiles": [{"name": "Enter", "type": "TEXT", "runnable": True, "data": venv_script}],
                    },
                },
            ],
            "steps": [
                {
                    "name": "GriptapeWorkflow",
                    "script": {
                        "actions": {
                            "onRun": {
                                "command": "python",
                                "args": [
                                    "{{Task.File.Run}}",
                                    "--input-file",
                                    "{{Param.InputFile}}",
                                    "--data-dir",
                                    "{{Param.LocationToRemap}}/assets",
                                ],
                            }
                        },
                        "embeddedFiles": [{"name": "Run", "type": "TEXT", "runnable": True, "data": python_script}],
                    },
                },
            ],
        }

        template_path = job_bundle_dir / "template.yaml"
        with template_path.open("w", encoding="utf-8") as template_file:
            yaml.dump(job_template, template_file, default_flow_style=False, sort_keys=False)

        logger.info("Job template written to: %s", template_path)

        return job_template

    @staticmethod
    def _generate_python_execution_script(library_paths: list[str]) -> str:
        """Generate the Python script that will execute the Griptape workflow."""
        library_paths_str = ", ".join(repr(path) for path in library_paths)

        return f"""import argparse
import json
import logging
import threading
import os
import sys
from multiprocessing import Queue as ProcessQueue
from pathlib import Path

from dotenv import load_dotenv

LIBRARIES = [str(Path(path)) for path in [{library_paths_str}]]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set up paths - use DataDir parameter for job attachments
job_assets_dir = Path("{{{{Param.LocationToRemap}}}}/assets")
synced_workflows_dir = Path("{{{{Param.LocationToRemap}}}}/synced_workflows")
synced_workflows_dir.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(job_assets_dir))

# Set HuggingFace home directory for model cache, and print
os.environ["HF_HOME"] = str(Path("{{{{Param.ModelsLocationToRemap}}}}"))
logger.info(f"HuggingFace model cache directory set to: {{os.environ['HF_HOME']}}")

# Load environment variables
if (job_assets_dir / ".env").exists():
    load_dotenv(str(job_assets_dir / ".env"))

def _set_config(libraries: list[str]) -> None:
    from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes  # noqa: PLC0415

    config_manager = GriptapeNodes.ConfigManager()
    config_manager.set_config_value(
        key="app_events.on_app_initialization_complete.libraries_to_register",
        value=libraries,
    )
    config_manager.set_config_value(
        key="workspace_directory",
        value="{{{{Param.LocationToRemap}}}}/output",
    )
    config_manager.set_config_value(
        key="synced_workflows_directory",
        value=str(synced_workflows_dir),
    )

    GriptapeNodes.LibraryManager().load_all_libraries_from_config()

_set_config(LIBRARIES)

from griptape_nodes.app.api import start_api
from griptape_nodes.app.app import _build_static_dir
from deadline_cloud_workflow_executor import DeadlineCloudWorkflowExecutor
from workflow import execute_workflow  # type: ignore[attr-defined]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-file",
        default=None,
        help="Path to JSON file containing input for the workflow",
    )
    parser.add_argument(
        "--data-dir",
        default=".",
        help="Directory containing job attachments and workflow files",
    )

    args = parser.parse_args()
    input_file_path = args.input_file
    data_dir = Path(args.data_dir)

    try:
        if input_file_path:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                flow_input = json.load(f)
            logger.info("Loaded input from file: %s", input_file_path)
        else:
            flow_input = {{}}
            logger.info("No input file provided, using empty input")
    except Exception as e:
        msg = f"Error reading JSON input file: {{e}}"
        logger.info(msg)
        raise

    static_dir = _build_static_dir()
    threading.Thread(target=lambda: start_api(static_dir), daemon=True).start()

    workflow_file_path = job_assets_dir / "workflow.py"
    workflow_runner = DeadlineCloudWorkflowExecutor()
    execute_workflow(
        input=flow_input,
        storage_backend="local",
        workflow_executor=workflow_runner,
    )
"""
