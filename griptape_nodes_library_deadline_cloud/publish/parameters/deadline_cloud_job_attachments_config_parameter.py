import logging
from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterGroup, ParameterMode
from griptape_nodes.exe_types.node_types import BaseNode
from griptape_nodes.traits.file_system_picker import FileSystemPicker

logger = logging.getLogger(__name__)


class DeadlineCloudJobAttachmentsConfigParameter:
    def __init__(
        self, node: BaseNode, metadata: dict[Any, Any] | None = None, allowed_modes: set[ParameterMode] | None = None
    ) -> None:
        self.node = node
        if metadata is None:
            metadata = {}
        metadata["showaddparameter"] = True
        attachment_input_paths = metadata.get("attachment_input_paths", [])
        attachment_output_paths = metadata.get("attachment_output_paths", [])

        # Add job config group
        with ParameterGroup(name="Job Attachments Config") as job_attachments_config_group:
            Parameter(
                name="attachment_input_paths",
                type="str",
                default_value=attachment_input_paths,
                tooltip="Input paths to attach files or directories to the Job.",
                allowed_modes=allowed_modes,
                traits={FileSystemPicker(allow_files=True, allow_directories=True, multiple=True)},
            )
            Parameter(
                name="attachment_output_paths",
                type="str",
                default_value=attachment_output_paths,
                tooltip="Output paths to use for the Job.",
                allowed_modes=allowed_modes,
                traits={FileSystemPicker(allow_files=False, allow_directories=True, multiple=True)},
            )

        job_attachments_config_group.ui_options = {"hide": False, "collapsed": True}
        self.node.add_node_element(job_attachments_config_group)

    @classmethod
    def get_param_names(cls) -> list[str]:
        return [
            "attachment_input_paths",
            "attachment_output_paths",
        ]
