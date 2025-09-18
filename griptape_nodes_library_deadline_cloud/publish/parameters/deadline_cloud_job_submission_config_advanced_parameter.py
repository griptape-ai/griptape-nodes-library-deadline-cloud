from typing import Any

from deadline.client.config import get_setting_default
from griptape_nodes.exe_types.core_types import Parameter, ParameterGroup, ParameterMode
from griptape_nodes.exe_types.node_types import BaseNode
from publish import DEADLINE_CLOUD_LIBRARY_CONFIG_KEY
from publish.base_deadline_cloud import BaseDeadlineCloud


class DeadlineCloudJobSubmissionConfigAdvancedParameter:
    def __init__(
        self, node: BaseNode, metadata: dict[Any, Any] | None = None, allowed_modes: set[ParameterMode] | None = None
    ) -> None:
        self.node = node
        if metadata is None:
            metadata = {}

        farm_id = metadata.get("farm_id", "")
        queue_id = metadata.get("queue_id", "")
        storage_profile_id = metadata.get("storage_profile_id", "")

        # Add advanced job config group
        with ParameterGroup(name="Job Submission Config Advanced") as job_submission_config_group_advanced:
            Parameter(
                name="priority",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=50,
                tooltip="The job priority for the Deadline Cloud Job.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="initial_state",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value="READY",
                tooltip="The initial state for the Deadline Cloud Job.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="max_failed_tasks",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=50,
                tooltip="The maximum number of failed tasks before the job is considered failed.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="max_task_retries",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=10,
                tooltip="The maximum number of task retries before the job is considered failed.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="farm_id",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=farm_id
                if farm_id != ""
                else BaseDeadlineCloud._get_config_value(
                    DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "farm_id", default=get_setting_default("defaults.farm_id")
                ),
                tooltip="The farm to use for the Deadline Cloud Job.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="queue_id",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=queue_id
                if queue_id != ""
                else BaseDeadlineCloud._get_config_value(
                    DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "queue_id", default=get_setting_default("defaults.queue_id")
                ),
                tooltip="The queue to use for the Deadline Cloud Job.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="storage_profile_id",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=storage_profile_id
                if storage_profile_id != ""
                else BaseDeadlineCloud._get_config_value(
                    DEADLINE_CLOUD_LIBRARY_CONFIG_KEY,
                    "storage_profile_id",
                    default=get_setting_default("settings.storage_profile_id"),
                ),
                tooltip="The storage profile ID for the Deadline Cloud Job.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="conda_channels",
                input_types=["str"],
                type="str",
                default_value="conda-forge",
                output_type="str",
                tooltip="Conda channels to install packages from.",
                allowed_modes=allowed_modes,
            )
            Parameter(
                name="conda_packages",
                input_types=["str"],
                type="str",
                default_value="python=3.12",
                output_type="str",
                tooltip="Conda packages install job.",
                allowed_modes=allowed_modes,
            )

        job_submission_config_group_advanced.ui_options = {"hide": False, "collapsed": True}
        self.node.add_node_element(job_submission_config_group_advanced)

    @classmethod
    def get_param_names(cls) -> list[str]:
        return [
            "priority",
            "initial_state",
            "max_failed_tasks",
            "max_task_retries",
            "farm_id",
            "queue_id",
            "storage_profile_id",
            "conda_channels",
            "conda_packages",
        ]
