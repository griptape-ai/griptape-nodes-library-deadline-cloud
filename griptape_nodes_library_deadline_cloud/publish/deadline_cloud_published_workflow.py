import json
import logging
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any

from botocore.exceptions import BotoCoreError, ClientError
from deadline.client.api import get_queue_user_boto3_session
from deadline.client.config import get_setting_default
from deadline.job_attachments.download import OutputDownloader
from deadline.job_attachments.models import JobAttachmentS3Settings
from griptape_nodes.app.app import _build_static_dir
from griptape_nodes.exe_types.core_types import Parameter, ParameterGroup, ParameterMode
from griptape_nodes.exe_types.node_types import AsyncResult, ControlNode
from publish import DEADLINE_CLOUD_LIBRARY_CONFIG_KEY
from publish.base_deadline_cloud import BaseDeadlineCloud

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DeadlineCloudPublishedWorkflow(ControlNode, BaseDeadlineCloud):
    def __init__(self, **kwargs) -> None:
        ControlNode.__init__(self, **kwargs)
        BaseDeadlineCloud.__init__(self, session=BaseDeadlineCloud._get_session())

        metadata = kwargs.get("metadata", {})

        # Store workflow shape and info
        attachments_dict = metadata.get("attachments", None)
        job_attachment_settings_dict = metadata.get("job_attachment_settings", None)

        self.attachments: dict | None = attachments_dict
        self.job_attachment_settings: dict | None = job_attachment_settings_dict
        self.job_template = metadata.get("job_template", {})
        self.relative_dir_path = metadata.get("relative_dir_path", "")
        self.workflow_shape = metadata.get("workflow_shape", {})

        with ParameterGroup(name="Job Submission Config") as submission_config_group:
            Parameter(
                name="job_name",
                input_types=["str"],
                type="str",
                default_value="",
                output_type="str",
                tooltip="The job name for the Deadline Cloud Job.",
            )
            Parameter(
                name="job_description",
                input_types=["str"],
                type="str",
                default_value="",
                output_type="str",
                tooltip="The job description for the Deadline Cloud Job.",
            )
            Parameter(
                name="priority",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=50,
                tooltip="The job priority for the Deadline Cloud Job.",
            )
            Parameter(
                name="initial_state",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value="READY",
                tooltip="The initial state for the Deadline Cloud Job.",
            )
            Parameter(
                name="max_failed_tasks",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=50,
                tooltip="The maximum number of failed tasks before the job is considered failed.",
            )
            Parameter(
                name="max_task_retries",
                input_types=["int"],
                type="int",
                output_type="int",
                default_value=10,
                tooltip="The maximum number of task retries before the job is considered failed.",
            )
            Parameter(
                name="farm_id",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=self._get_config_value(
                    DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "farm_id", default=get_setting_default("defaults.farm_id")
                ),
                tooltip="The farm ID for the Deadline Cloud Job.",
            )
            Parameter(
                name="queue_id",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value=self._get_config_value(
                    DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "queue_id", default=get_setting_default("defaults.queue_id")
                ),
                tooltip="The queue ID for the Deadline Cloud Job.",
            )

        submission_config_group.ui_options = {"hide": True}  # Hide the job config group by default.
        self.add_node_element(submission_config_group)

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
        job_config_group.ui_options = {"hide": True}  # Hide the job config group by default.
        self.add_node_element(job_config_group)

    @classmethod
    def get_job_submission_parameter_names(cls) -> list[str]:
        """Get the names of the job submission parameters."""
        return [
            "job_name",
            "job_description",
            "priority",
            "initial_state",
            "max_failed_tasks",
            "max_task_retries",
            "farm_id",
            "queue_id",
        ]

    def validate_before_workflow_run(self) -> list[Exception] | None:
        exceptions = super().validate_before_workflow_run() or []

        try:
            if not self.get_parameter_value("job_template"):
                msg = "Job template is not set. Configure the Node with a valid Deadline Cloud Job Template before running."
                exceptions.append(ValueError(msg))

            if not self.get_parameter_value("job_attachment_settings"):
                msg = "Job attachment settings are not set. Configure the Node with valid Job Attachment Settings before running."
                exceptions.append(ValueError(msg))

            if not self.get_parameter_value("attachments"):
                msg = "Attachments are not set. Configure the Node with valid Attachments before running."
                exceptions.append(ValueError(msg))

        except Exception as e:
            # Add any exceptions to your list to return
            exceptions.append(e)

        # if there are exceptions, they will display when the user tries to run the flow with the node.
        return exceptions if exceptions else None

    def _submit_job_with_attachments(
        self,
        attachments: dict[str, Any],
        farm_id: str,
        queue_id: str,
        job_template: dict[str, Any],
        job_parameters: dict[str, Any] | None = None,
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

            # Create job with attachments
            response = deadline_client.create_job(
                farmId=farm_id,
                queueId=queue_id,
                template=job_template_str,
                templateType="JSON",
                parameters=job_parameters if job_parameters is not None else {},
                priority=priority,
                maxFailedTasksCount=max_failed_tasks,
                maxRetriesPerTask=max_task_retries,
                targetTaskRunStatus=initial_state,
                attachments=attachments,
            )

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
        job_completed = False
        deadline_client = self._get_client()
        job_details: Any = {}

        while not job_completed:
            job_details = deadline_client.get_job(jobId=job_id, queueId=queue_id, farmId=farm_id)
            status = job_details.get("taskRunStatus", "UNKNOWN")
            msg = f"Task Run Status for Job ID {job_id}: {status}"
            logger.info(msg)

            if status in ["SUCCEEDED", "FAILED", "CANCELED", "NOT_COMPATIBLE"]:
                break
            time.sleep(1)

        return job_details

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
                elif output_file.startswith("output/staticfiles/"):
                    static_file_path = Path(root_path) / output_file
                    static_dir = _build_static_dir()
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
        downloader = OutputDownloader(
            s3_settings=job_attachment_settings,
            farm_id=farm_id,
            queue_id=queue_id,
            job_id=job_id,
            session=self._session,
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

        return job_template

    def _upload_input_json_to_s3(self, input_json: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Upload input JSON to S3 as a job attachment and return the relative path."""
        try:
            from publish.deadline_cloud_publisher import DeadlineCloudPublisher

            temp_dir = Path(tempfile.mkdtemp(prefix="input_json_"))
            input_json_path = temp_dir / "input.json"

            with input_json_path.open("w", encoding="utf-8") as f:
                json.dump(input_json, f, indent=2)

            logger.info("Created input JSON file at: %s", input_json_path)

            farm_id = self.get_parameter_value("farm_id")
            queue_id = self.get_parameter_value("queue_id")
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
        combined = original_attachments.copy()

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

    def _process(self) -> None:
        attachments = self.get_parameter_value("attachments")
        job_template = self.get_parameter_value("job_template")
        relative_dir_path = self.get_parameter_value("relative_dir_path")
        farm_id = self.get_parameter_value("farm_id")
        queue_id = self.get_parameter_value("queue_id")

        root_dir = str(attachments["manifests"][0]["rootPath"])
        input_json = self._collect_input_parameters()

        # Upload input JSON to S3 to avoid parameter size limits
        logger.info("Uploading input JSON to S3 to avoid parameter size limits")
        input_json_path, input_attachments = self._upload_input_json_to_s3(input_json)

        # Combine the original attachments with the input JSON attachments
        combined_attachments = self._combine_attachments(attachments, input_attachments)

        job_parameters = {
            "InputFile": {"path": input_json_path},
            "DataDir": {"path": root_dir},
            "LocationToRemap": {"path": relative_dir_path},
        }

        job_template = self._reconcile_job_template(job_template)
        job_id = self._submit_job_with_attachments(
            attachments=combined_attachments,
            farm_id=farm_id,
            queue_id=queue_id,
            job_template=job_template,
            job_parameters=job_parameters,
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

    def process(
        self,
    ) -> AsyncResult[None]:
        yield lambda: self._process()
