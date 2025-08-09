from typing import Any

from deadline.client.config import get_setting_default
from griptape_nodes.exe_types.core_types import Parameter, ParameterGroup, ParameterMode
from griptape_nodes.exe_types.node_types import StartNode
from publish import DEADLINE_CLOUD_LIBRARY_CONFIG_KEY
from publish.base_deadline_cloud import BaseDeadlineCloud


class DeadlineCloudStartFlow(StartNode):
    def __init__(
        self,
        name: str,
        metadata: dict[Any, Any] | None = None,
    ) -> None:
        if metadata is None:
            metadata = {}
        metadata["showaddparameter"] = True
        super().__init__(name, metadata)

        # Add job config group
        with ParameterGroup(name="Job Submission Config") as job_submission_config_group:
            Parameter(
                name="job_name",
                input_types=["str"],
                type="str",
                output_type="str",
                tooltip="The job name for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )
            Parameter(
                name="job_description",
                input_types=["str"],
                type="str",
                output_type="str",
                tooltip="The job description for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )

        job_submission_config_group.ui_options = {"hide": False}
        self.add_node_element(job_submission_config_group)

        # Add advanced job config group
        with ParameterGroup(name="Job Submission Config Advanced") as job_submission_config_group_advanced:
            Parameter(
                name="priority",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=50,
                tooltip="The job priority for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )
            Parameter(
                name="initial_state",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value="READY",
                tooltip="The initial state for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )
            Parameter(
                name="max_failed_tasks",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=50,
                tooltip="The maximum number of failed tasks before the job is considered failed.",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )
            Parameter(
                name="max_task_retries",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=10,
                tooltip="The maximum number of task retries before the job is considered failed.",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )
            Parameter(
                name="farm_id",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=BaseDeadlineCloud._get_config_value(
                    DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "farm_id", default=get_setting_default("defaults.farm_id")
                ),
                tooltip="The farm to use for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )
            Parameter(
                name="queue_id",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=BaseDeadlineCloud._get_config_value(
                    DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "queue_id", default=get_setting_default("defaults.queue_id")
                ),
                tooltip="The queue to use for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )

        job_submission_config_group_advanced.ui_options = {"hide": False, "collapsed": True}
        self.add_node_element(job_submission_config_group_advanced)

    def process(self) -> None:
        pass
