from __future__ import annotations

import copy
import json
import logging
import shutil
import tempfile
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any

from botocore.exceptions import BotoCoreError, ClientError
from deadline.client.api import get_queue_user_boto3_session
from deadline.job_attachments.download import OutputDownloader
from deadline.job_attachments.models import JobAttachmentS3Settings
from griptape_nodes.exe_types.core_types import Parameter, ParameterGroup, ParameterMessage, ParameterMode
from griptape_nodes.exe_types.node_types import AsyncResult, SuccessFailureNode
from griptape_nodes.exe_types.param_components.execution_status_component import ExecutionStatusComponent
from publish.base_deadline_cloud import BaseDeadlineCloud
from publish.deadline_cloud_job_poller import DeadlineCloudJobDetails, DeadlineCloudJobPoller
from publish.parameters.deadline_cloud_host_config_parameter import DeadlineCloudHostConfigParameter
from publish.parameters.deadline_cloud_job_submission_config_advanced_parameter import (
    DeadlineCloudJobSubmissionConfigAdvancedParameter,
)
from publish.parameters.deadline_cloud_job_submission_config_parameter import DeadlineCloudJobSubmissionConfigParameter

if TYPE_CHECKING:
    from deadline.job_attachments.models import StorageProfile


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PublishedWorkflowExecutionStatus(StrEnum):
    """Status enum for published workflow execution."""

    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    FAILURE = "FAILURE"


class DeadlineCloudPublishedWorkflow(SuccessFailureNode, BaseDeadlineCloud):
    def __init__(self, **kwargs) -> None:
        SuccessFailureNode.__init__(self, **kwargs)
        BaseDeadlineCloud.__init__(self, session=BaseDeadlineCloud._get_session())

        metadata = kwargs.get("metadata", {})

        # Store workflow shape and info
        attachments_dict = metadata.get("attachments", None)
        job_attachment_settings_dict = metadata.get("job_attachment_settings", None)

        self.attachments: dict | None = attachments_dict
        self.job_attachment_settings: dict | None = job_attachment_settings_dict
        self.job_template = metadata.get("job_template", {})
        self.relative_dir_path = metadata.get("relative_dir_path", "")
        self.models_dir_path = metadata.get("models_dir_path", "")
        self.workflow_shape = metadata.get("workflow_shape", {})

        if attachments_dict is None or job_attachment_settings_dict is None:
            self.add_node_element(
                ParameterMessage(
                    name="deadline_cloud_published_workflow_parameter_message",
                    title="Deadline Cloud Published Workflow Configuration Warning",
                    variant="warning",
                    value=self.get_help_message(),
                )
            )

        # Add job config group
        self.job_submission_config_params = DeadlineCloudJobSubmissionConfigParameter(self, metadata)

        # Add advanced job config group
        self._job_submission_config_advanced_params = DeadlineCloudJobSubmissionConfigAdvancedParameter(self, metadata)

        # Add host config group
        self._host_config_params = DeadlineCloudHostConfigParameter(self)
        self._host_config_params.set_host_config_param_visibility(visible=False)

        # Add job config group
        with ParameterGroup(name="Job Config") as job_config_group:
            Parameter(
                name="attachments",
                input_types=["dict"],
                type="dict",
                output_type="dict",
                default_value=self.attachments if self.attachments else {},
                tooltip="The attachments for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT},
            )
            Parameter(
                name="job_attachment_settings",
                input_types=["dict"],
                type="dict",
                output_type="dict",
                default_value=self.job_attachment_settings if self.job_attachment_settings else {},
                tooltip="The job attachment settings for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT},
            )
            Parameter(
                name="job_template",
                input_types=["dict"],
                type="dict",
                output_type="dict",
                default_value=self.job_template,
                tooltip="The job template for the Deadline Cloud Job.",
                allowed_modes={ParameterMode.OUTPUT},
            )
            Parameter(
                name="relative_dir_path",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=self.relative_dir_path,
                tooltip="Relative path for the workflow files.",
                allowed_modes={ParameterMode.OUTPUT},
            )
            Parameter(
                name="models_dir_path",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=self.models_dir_path,
                tooltip="Relative path for the models directory.",
                allowed_modes={ParameterMode.OUTPUT},
            )
        job_config_group.ui_options = {"hide": True}  # Hide the job config group by default.
        self.add_node_element(job_config_group)

        # Add status parameters
        self.status_component = ExecutionStatusComponent(
            self,
            was_successful_modes={ParameterMode.PROPERTY},
            result_details_modes={ParameterMode.OUTPUT},
            parameter_group_initially_collapsed=False,
            result_details_tooltip="Details about the published workflow execution result",
            result_details_placeholder="Details on the published workflow execution will be presented here.",
        )

    def get_help_message(self) -> str:
        return (
            "The Deadline Cloud Published Workflow node is intended to be auto-generated via publishing a Workflow.\n\n "
            "To publish a Workflow to Deadline Cloud, you can:\n"
            "   1. Configure a Workflow in the GUI with the Deadline Cloud Start Flow and End Flow Nodes\n"
            "   2. Click the 'Publish' button (rocket icon, top right) to publish the workflow to Deadline Cloud\n"
            "   3. Open the resulting Workflow in the GUI, which will have the Deadline Cloud Published Workflow node configured"
        )

    def after_value_set(self, parameter: Parameter, value: Any) -> None:
        if parameter.name == "run_on_all_worker_hosts":
            self._host_config_params.set_host_config_param_visibility(visible=not value)
        self._job_submission_config_advanced_params.after_value_set(parameter, value)

    @classmethod
    def get_default_node_parameter_names(cls) -> list[str]:
        """Get the names of the parameters configured on the node by default."""
        params = DeadlineCloudJobSubmissionConfigParameter.get_param_names()
        params.extend(DeadlineCloudJobSubmissionConfigAdvancedParameter.get_param_names())
        params.extend(DeadlineCloudHostConfigParameter.get_param_names())
        # Execution Status Component parameters
        params.extend(["was_successful", "result_details"])
        return params

    def validate_before_workflow_run(self) -> list[Exception] | None:
        exceptions = super().validate_before_workflow_run() or []

        try:
            job_template = self.get_parameter_value("job_template")
            if not job_template or len(job_template) == 0:
                msg = "Job template is not set. Configure the Node with a valid Deadline Cloud Job Template before running."
                exceptions.append(ValueError(msg))

            job_attachment_settings = self.get_parameter_value("job_attachment_settings")
            if job_attachment_settings is None or len(job_attachment_settings) == 0:
                msg = "Job attachment settings are not set. Configure the Node with valid Job Attachment Settings before running."
                exceptions.append(ValueError(msg))

            attachments = self.get_parameter_value("attachments")
            if attachments is None or len(attachments) == 0:
                msg = "Attachments are not set. Configure the Node with valid Attachments before running."
                exceptions.append(ValueError(msg))

            farm_id = self.get_parameter_value("farm_id")
            if farm_id is None or farm_id == "":
                msg = "Farm ID is not set. Configure the Node with a valid Farm ID before running."
                exceptions.append(ValueError(msg))

            queue_id = self.get_parameter_value("queue_id")
            if queue_id is None or queue_id == "":
                msg = "Queue ID is not set. Configure the Node with a valid Queue ID before running."
                exceptions.append(ValueError(msg))

            if farm_id and queue_id:
                farm_queue_exception = self._validate_farm_and_queue_permissions(farm_id, queue_id)
                if farm_queue_exception:
                    exceptions.append(farm_queue_exception)

        except Exception as e:
            # Add any exceptions to your list to return
            exceptions.append(e)

        # if there are exceptions, they will display when the user tries to run the flow with the node.
        return exceptions if exceptions else None

    def _validate_farm_and_queue_permissions(self, farm_id: str, queue_id: str) -> Exception | None:
        """Validate that the user has permissions to the specified farm and queue."""
        try:
            # Validate farm access
            self.search_jobs(farm_id=farm_id, queue_id=queue_id, page_size=1)

        except (ClientError, BotoCoreError) as e:
            details = f"AWS API error validating farm and queue permissions: {e}"
            logger.error(details)
            return RuntimeError(details)
        except Exception as e:
            details = f"Unexpected error validating farm and queue permissions: {e}"
            logger.exception(details)
            return RuntimeError(details)

    def _submit_job_with_attachments(  # noqa: PLR0913
        self,
        attachments: dict[str, Any],
        farm_id: str,
        queue_id: str,
        job_template: dict[str, Any],
        job_parameters: dict[str, Any] | None = None,
        storage_profile: StorageProfile | None = None,
    ) -> str:
        """Submit job to Deadline Cloud with processed attachments."""
        try:
            job_template_str = json.dumps(job_template)
            deadline_client = self._get_client()
            logger.info("Submitting job to farm %s, queue %s", farm_id, queue_id)

            priority = self.get_parameter_value("priority")
            max_failed_tasks = self.get_parameter_value("max_failed_tasks")
            max_task_retries = self.get_parameter_value("max_task_retries")
            initial_state = self.get_parameter_value("initial_state")

            create_job_kwargs = {
                "farmId": farm_id,
                "queueId": queue_id,
                "template": job_template_str,
                "templateType": "JSON",
                "parameters": job_parameters if job_parameters is not None else {},
                "priority": priority,
                "maxFailedTasksCount": max_failed_tasks,
                "maxRetriesPerTask": max_task_retries,
                "targetTaskRunStatus": initial_state,
                "attachments": attachments,
            }
            if storage_profile is not None:
                create_job_kwargs["storageProfileId"] = storage_profile.storageProfileId

            # Create job with attachments
            response = deadline_client.create_job(**create_job_kwargs)

            job_id = response["jobId"]
            logger.info("Job submitted successfully with ID: %s", job_id)

        except (ClientError, BotoCoreError) as e:
            details = f"AWS API error submitting job: {e}"
            logger.error(details)
            raise RuntimeError(details) from e
        except OSError as e:
            details = f"File system error submitting job: {e}"
            logger.error(details)
            raise RuntimeError(details) from e
        except Exception as e:
            details = f"Unexpected error submitting job: {e}"
            logger.exception(details)
            raise RuntimeError(details) from e

        return job_id

    def _poll_job(self, job_id: str, queue_id: str, farm_id: str) -> Any:
        def status_callback(job_details: DeadlineCloudJobDetails, elapsed_time: float) -> None:
            self.append_value_to_parameter(
                parameter_name=self.status_component._result_details.name,
                value=f"\nJob Status - Lifecycle: {job_details.lifecycle_status}, Task Status: {job_details.task_run_status}, Elapsed Time: {elapsed_time}s",
            )

        poller = DeadlineCloudJobPoller(
            client=self._get_client(),
            config=self._get_config_parser(),
            job_id=job_id,
            queue_id=queue_id,
            farm_id=farm_id,
            max_poll_interval=10,
            status_callback=status_callback,
        )
        return poller.poll_job()

    def _get_static_files_directory(self) -> Path:
        from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

        workspace_dir = GriptapeNodes.ConfigManager().get_config_value("workspace_directory")
        static_files_dir = GriptapeNodes.ConfigManager().get_config_value("static_files_directory")

        return Path(workspace_dir) / static_files_dir

    def _extract_workflow_output_from_output_paths(self, output_paths: dict[str, list[str]]) -> dict:
        """Extract workflow output from the output paths."""
        # output_paths is a dictionary of root paths to output file paths like:
        # {'/var/folders/3v/jg416m5115j47dxwzznmqfhc0000gn/T/flowy_deadline_bundle_3s0cvl9d': ['output/workflow_output.json']}  # noqa: ERA001

        workflow_output = {}
        for root_path, output_files in output_paths.items():
            for output_file in output_files:
                if output_file.endswith("workflow_output.json"):
                    workflow_file_path = Path(root_path) / output_file
                    with workflow_file_path.open(encoding="utf-8") as f:
                        workflow_output = json.load(f)
                    workflow_file_path.unlink(missing_ok=True)  # Remove the workflow output file after reading
                elif "output" in output_file and "staticfiles" in output_file:
                    static_file_path = Path(root_path) / output_file
                    static_dir = self._get_static_files_directory()
                    # Copy the static file to the static directory
                    shutil.copy(static_file_path, static_dir / static_file_path.name)

        return workflow_output

    def _collect_input_parameters(self) -> dict[str, dict[str, Any]]:
        """Collect input parameters and structure them for the published workflow."""
        input_json = {}

        if "input" not in self.workflow_shape:
            return input_json

        for node_name, node_params in self.workflow_shape["input"].items():
            if isinstance(node_params, dict):
                node_inputs = {}
                for param_name in node_params:
                    param_value = self.get_parameter_value(param_name)

                    if param_value is not None:
                        node_inputs[param_name] = param_value

                if node_inputs:
                    input_json[node_name] = node_inputs

        return input_json

    def _get_workflow_output(self, farm_id: str, job_id: str, queue_id: str) -> dict[str, Any]:
        """Download and return the workflow output from the job."""
        deadline_client = self._get_client()
        queue_response = deadline_client.get_queue(farmId=farm_id, queueId=queue_id)
        job_attachment_settings = JobAttachmentS3Settings(**queue_response["jobAttachmentSettings"])

        queue_session = get_queue_user_boto3_session(
            deadline_client,
            None,
            farm_id,
            queue_id,
        )

        downloader = OutputDownloader(
            s3_settings=job_attachment_settings,
            farm_id=farm_id,
            queue_id=queue_id,
            job_id=job_id,
            session=queue_session,
        )

        def on_download_progress(progress: Any) -> bool:
            logger.info("Uploading assets: %s", progress)
            return True  # Continue downloading

        try:
            output = downloader.download_job_output(
                on_downloading_files=on_download_progress,
            )
            logger.info(downloader.get_output_paths_by_root())
            logger.info("Workflow output downloaded successfully.")
            logger.info(output)

            output_paths_by_root = downloader.get_output_paths_by_root()
            return self._extract_workflow_output_from_output_paths(output_paths_by_root)
        except Exception as e:
            details = f"Error downloading workflow output: {e}"
            logger.error(details)
            raise RuntimeError(details) from e

    def _map_output_parameters(self, output: dict[str, Any] | None) -> None:
        """Map job output to output parameters."""
        if not output or "output" not in self.workflow_shape:
            return

        logger.info("Mapping output parameters for job with output: %s", output)

        for node_name, node_params in self.workflow_shape["output"].items():
            logger.info("Processing node '%s' with parameters: %s", node_name, node_params)
            if isinstance(node_params, dict) and node_name in output:
                node_outputs = output[node_name]
                logger.info("Node '%s' outputs: %s", node_name, node_outputs)
                if isinstance(node_outputs, dict):
                    for param_name in node_params:
                        logger.info("Checking parameter '%s' in node '%s'", param_name, node_name)
                        # Check if this parameter exists in the output
                        if param_name in node_outputs:
                            param_value = node_outputs[param_name]
                            logger.info("Found output parameter '%s' with value: %s", param_name, param_value)

                            # Set the output parameter value
                            self.set_parameter_value(
                                param_name=param_name,
                                value=param_value,
                            )
                            self.parameter_output_values[param_name] = param_value
                            logger.info("Set output parameter %s = %s", param_name, param_value)

    def _reconcile_job_template(self, job_template: dict[str, Any]) -> dict[str, Any]:
        """Reconcile the job template with the parameters."""
        job_name = self.get_parameter_value("job_name")
        if job_name:
            job_template["name"] = job_name

        job_description = self.get_parameter_value("job_description")
        if job_description:
            job_template["description"] = job_description

        job_template = self._reconcile_job_template_host_config(job_template)

        return job_template

    def _reconcile_job_template_host_config(self, job_template: dict[str, Any]) -> dict[str, Any]:
        """Reconcile the job template with the host configuration."""
        run_on_all_worker_hosts = self.get_parameter_value("run_on_all_worker_hosts")
        if not run_on_all_worker_hosts:
            host_config = self._host_config_params.get_host_config_job_template_dict()
            if len(host_config) > 0:
                for step in job_template["steps"]:
                    step["hostRequirements"] = copy.deepcopy(host_config)

        return job_template

    def _upload_input_json_to_s3(
        self, input_json: dict[str, Any], farm_id: str, queue_id: str, storage_profile: StorageProfile | None = None
    ) -> tuple[str, dict[str, Any]]:
        """Upload input JSON to S3 as a job attachment and return the relative path."""
        try:
            from publish.deadline_cloud_publisher import DeadlineCloudPublisher

            temp_dir = Path(tempfile.mkdtemp(prefix="input_json_"))
            input_json_path = temp_dir / "input.json"

            with input_json_path.open("w", encoding="utf-8") as f:
                json.dump(input_json, f, indent=2)

            logger.info("Created input JSON file at: %s", input_json_path)
            deadline_client = self._get_client()

            queue_response = deadline_client.get_queue(farmId=farm_id, queueId=queue_id)
            job_attachment_settings = JobAttachmentS3Settings(**queue_response["jobAttachmentSettings"])

            queue_session = get_queue_user_boto3_session(
                deadline_client,
                None,
                farm_id,
                queue_id,
            )
            queue_session._session.set_config_variable("region", self._session.region_name)

            input_attachments = DeadlineCloudPublisher.upload_paths_as_job_attachments(
                input_paths=[str(input_json_path)],
                output_paths=[],
                farm_id=farm_id,
                queue_id=queue_id,
                storage_profile=storage_profile,
                job_attachment_settings=job_attachment_settings,
                queue_session=queue_session,
            )

            logger.info("Input JSON uploaded successfully to S3")

            # Return the relative path and the attachments
            return str(input_json_path), input_attachments.to_dict()
        except Exception as e:
            details = f"Error uploading input JSON to S3: {e}"
            logger.error(details)
            raise RuntimeError(details) from e

    def _combine_attachments(
        self, original_attachments: dict[str, Any], input_attachments: dict[str, Any]
    ) -> dict[str, Any]:
        """Combine original workflow attachments with input JSON attachments."""
        combined = copy.deepcopy(original_attachments)

        # Add the input JSON manifest to the existing manifests
        if input_attachments.get("manifests"):
            if "manifests" not in combined:
                combined["manifests"] = []
            combined["manifests"].extend(input_attachments["manifests"])

        logger.info(
            "Combined %d original manifests with %d input manifests",
            len(original_attachments.get("manifests", [])),
            len(input_attachments.get("manifests", [])),
        )

        return combined

    def _handle_execution_result(
        self,
        status: PublishedWorkflowExecutionStatus,
        input_path: Path | None,
        output_path: Path | None,
        details: str,
        exception: Exception | None = None,
    ) -> None:
        """Handle execution result for all cases."""
        match status:
            case PublishedWorkflowExecutionStatus.FAILURE:
                failure_details = f"Published Workflow execution failed\nError: {details}"

                if exception:
                    failure_details += f"\nException type: {type(exception).__name__}"
                    if exception.__cause__:
                        failure_details += f"\nCause: {exception.__cause__}"

                self._set_status_results(was_successful=False, result_details=f"{status}: {failure_details}")
                msg = f"Error executing published workflow: {details}"
                logger.error(msg)

            case PublishedWorkflowExecutionStatus.SUCCESS:
                result_details = f"Published Workflow executed successfully\nOutput path: {output_path}\n"
                if input_path and input_path.exists():
                    result_details += f"Input path: {input_path}\n"
                if output_path and output_path.exists():
                    result_details += f"Output path: {output_path}\n"

                self._set_status_results(was_successful=True, result_details=f"{status}: {result_details}")

    def _handle_error_with_graceful_exit(
        self, error_details: str, exception: Exception, input_path: Path | None, output_path: Path | None
    ) -> None:
        """Handle error with graceful exit if failure output is connected."""
        self._handle_execution_result(
            status=PublishedWorkflowExecutionStatus.FAILURE,
            input_path=input_path,
            output_path=output_path,
            details=error_details,
            exception=exception,
        )
        # Use the helper to handle exception based on connection status
        self._handle_failure_exception(RuntimeError(error_details))

    def _process(self) -> None:
        # Reset execution state and result details at the start of each run
        self._clear_execution_status()
        input_path: Path | None = None
        output_path: Path | None = None

        try:
            attachments = self.get_parameter_value("attachments")
            job_template = self.get_parameter_value("job_template")
            relative_dir_path = self.get_parameter_value("relative_dir_path")
            models_dir_path = self.get_parameter_value("models_dir_path")
            farm_id = self.get_parameter_value("farm_id")
            queue_id = self.get_parameter_value("queue_id")
            storage_profile_id = self.get_parameter_value("storage_profile_id")

            root_dir = str(attachments["manifests"][0]["rootPath"])
            input_json = self._collect_input_parameters()

            storage_profile: StorageProfile | None = self._get_storage_profile_for_queue(
                farm_id, queue_id, storage_profile_id
            )

            # Upload input JSON to S3 to avoid parameter size limits
            logger.info("Uploading input JSON to S3 to avoid parameter size limits")
            input_json_path, input_attachments = self._upload_input_json_to_s3(
                input_json, farm_id, queue_id, storage_profile
            )
            input_path = Path(input_json_path).parent
            output_path = input_path / "output"

            # Combine the original attachments with the input JSON attachments
            combined_attachments = self._combine_attachments(attachments, input_attachments)

            job_parameters = {
                "InputFile": {"path": input_json_path},
                "DataDir": {"path": root_dir},
                "LocationToRemap": {"path": relative_dir_path},
                "ModelsLocationToRemap": {"path": models_dir_path},
                "CondaChannels": {"string": self.get_parameter_value("conda_channels")},
                "CondaPackages": {"string": self.get_parameter_value("conda_packages")},
            }

            job_template = self._reconcile_job_template(job_template)
            job_id = self._submit_job_with_attachments(
                attachments=combined_attachments,
                farm_id=farm_id,
                queue_id=queue_id,
                job_template=job_template,
                job_parameters=job_parameters,
                storage_profile=storage_profile,
            )

            self._poll_job(
                job_id=job_id,
                queue_id=queue_id,
                farm_id=farm_id,
            )

            output = self._get_workflow_output(
                farm_id=farm_id,
                job_id=job_id,
                queue_id=queue_id,
            )
            self._map_output_parameters(output)

            input_path = Path(input_json_path)
            if input_path.exists():
                input_path.unlink(missing_ok=True)
                shutil.rmtree(input_path.parent, ignore_errors=True)

            self._handle_execution_result(
                status=PublishedWorkflowExecutionStatus.SUCCESS,
                input_path=input_path,
                output_path=output_path,
                details=f"Published workflow executed successfully with Job ID: {job_id}",
            )
        except Exception as e:
            details = f"Error during published workflow execution: {e}"
            logger.exception(details)
            self._handle_error_with_graceful_exit(details, e, input_path, output_path)
            return

    def process(
        self,
    ) -> AsyncResult[None]:
        yield lambda: self._process()
