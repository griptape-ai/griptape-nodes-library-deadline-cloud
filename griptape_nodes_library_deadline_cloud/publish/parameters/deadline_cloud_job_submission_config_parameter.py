from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterGroup, ParameterMode
from griptape_nodes.exe_types.node_types import BaseNode


class DeadlineCloudJobSubmissionConfigParameter:
    def __init__(
        self, node: BaseNode, metadata: dict[Any, Any] | None = None, allowed_modes: set[ParameterMode] | None = None
    ) -> None:
        self.node = node
        if metadata is None:
            metadata = {}
        metadata["showaddparameter"] = True
        job_name = metadata.get("job_name", "")
        job_description = metadata.get("job_description", "")

        # Add job config group
        with ParameterGroup(name="Job Submission Config") as job_submission_config_group:
            Parameter(
                name="job_name",
                input_types=["str"],
                type="str",
                default_value=job_name,
                output_type="str",
                tooltip="The job name for the Deadline Cloud Job.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="job_description",
                input_types=["str"],
                type="str",
                default_value=job_description,
                output_type="str",
                tooltip="The job description for the Deadline Cloud Job.",
                allowed_modes=allowed_modes,
            )

        job_submission_config_group.ui_options = {"hide": False}
        self.node.add_node_element(job_submission_config_group)

    @classmethod
    def get_param_names(cls) -> list[str]:
        return [
            "job_name",
            "job_description",
        ]
