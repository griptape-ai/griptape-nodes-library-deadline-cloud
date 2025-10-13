import logging
from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import StartNode
from publish.parameters.deadline_cloud_host_config_parameter import DeadlineCloudHostConfigParameter
from publish.parameters.deadline_cloud_job_attachments_config_parameter import (
    DeadlineCloudJobAttachmentsConfigParameter,
)
from publish.parameters.deadline_cloud_job_submission_config_advanced_parameter import (
    DeadlineCloudJobSubmissionConfigAdvancedParameter,
)
from publish.parameters.deadline_cloud_job_submission_config_parameter import DeadlineCloudJobSubmissionConfigParameter

logger = logging.getLogger(__name__)


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
        self._job_submission_config_params = DeadlineCloudJobSubmissionConfigParameter(
            self, metadata, allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY}
        )

        # Add job attachments config group
        self._job_attachments_config_params = DeadlineCloudJobAttachmentsConfigParameter(
            self, metadata, allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY}
        )

        # Add advanced job config group
        self._job_submission_config_advanced_params = DeadlineCloudJobSubmissionConfigAdvancedParameter(
            self, metadata, allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY}
        )

        # Add host config group
        self._host_config_params = DeadlineCloudHostConfigParameter(
            self, allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY}
        )
        self._host_config_params.set_host_config_param_visibility(visible=False)

    def after_value_set(self, parameter: Parameter, value: Any) -> None:
        if parameter.name == "run_on_all_worker_hosts":
            self._host_config_params.set_host_config_param_visibility(visible=not value)
        self._job_submission_config_advanced_params.after_value_set(parameter, value)

    def process(self) -> None:
        pass
