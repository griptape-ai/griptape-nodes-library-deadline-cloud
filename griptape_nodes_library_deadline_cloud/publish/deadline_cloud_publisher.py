from __future__ import annotations

import importlib.metadata
import json
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from botocore.exceptions import BotoCoreError, ClientError
from deadline.client.api import get_queue_user_boto3_session
from deadline.client.config import get_setting_default
from deadline.client.config.config_file import get_cache_directory
from deadline.job_attachments.models import Attachments, JobAttachmentS3Settings
from deadline.job_attachments.upload import S3AssetManager, S3AssetUploader
from dotenv import set_key
from dotenv.main import DotEnv
from griptape_nodes.exe_types.node_types import BaseNode, StartNode
from griptape_nodes.node_library.library_registry import LibraryNameAndVersion, LibraryRegistry
from griptape_nodes.node_library.workflow_registry import Workflow, WorkflowRegistry
from griptape_nodes.retained_mode.events.app_events import (
    GetEngineVersionRequest,
    GetEngineVersionResultSuccess,
)
from griptape_nodes.retained_mode.events.flow_events import (
    GetTopLevelFlowRequest,
    GetTopLevelFlowResultSuccess,
    ListNodesInFlowRequest,
    ListNodesInFlowResultSuccess,
)
from griptape_nodes.retained_mode.events.node_events import (
    SerializeNodeToCommandsRequest,
    SerializeNodeToCommandsResultSuccess,
)
from griptape_nodes.retained_mode.events.parameter_events import (
    GetParameterValueRequest,
    GetParameterValueResultSuccess,
)
from griptape_nodes.retained_mode.events.secrets_events import (
    GetAllSecretValuesRequest,
    GetAllSecretValuesResultSuccess,
)
from griptape_nodes.retained_mode.events.workflow_events import (
    PublishWorkflowResultFailure,
    PublishWorkflowResultSuccess,
    SaveWorkflowRequest,
    SaveWorkflowResultSuccess,
)
from griptape_nodes.retained_mode.griptape_nodes import (
    GriptapeNodes,
    Version,
)
from huggingface_hub.constants import HF_HUB_CACHE
from publish import DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, LIBRARY_NAME
from publish.base_deadline_cloud import BaseDeadlineCloud
from publish.deadline_cloud_job_template_generator import (
    DeadlineCloudJobTemplateGenerator,
)
from publish.deadline_cloud_workflow_builder import (
    DeadlineCloudWorkflowBuilder,
    DeadlineCloudWorkflowBuilderInput,
)

if TYPE_CHECKING:
    from boto3 import Session
    from deadline.job_attachments.models import StorageProfile
    from griptape_nodes.retained_mode.events.base_events import ResultPayload
    from griptape_nodes.retained_mode.managers.library_manager import LibraryManager
    from publish.deadline_cloud_start_flow import DeadlineCloudStartFlow


T = TypeVar("T")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deadline_cloud_publisher")


class DeadlineCloudPublisher(BaseDeadlineCloud):
    def __init__(
        self,
        workflow_name: str,
        *,
        execute_on_publish: bool = False,
        published_workflow_file_name: str | None = None,
        pickle_control_flow_result: bool = False,
    ) -> None:
        super().__init__(session=BaseDeadlineCloud._get_session())
        self._workflow_name = workflow_name
        self._published_workflow_file_name = published_workflow_file_name or f"{self._workflow_name}_aws_dc_executor"
        self.execute_on_publish = execute_on_publish
        self._job_template: dict[str, Any] = {}
        self._deadline_cloud_start_flow_node_commands: SerializeNodeToCommandsResultSuccess | None = None
        self._unique_parameter_uuid_to_values: dict = {}
        self._set_parameter_value_commands_per_node: dict = {}
        self._node_name_to_uuid: dict = {}
        self.pickle_control_flow_result = pickle_control_flow_result

    def publish_workflow(self) -> ResultPayload:
        try:
            # Ensure the workflow file exists
            self._validate_workflow(self._workflow_name)

            # Get the workflow shape
            workflow_shape = GriptapeNodes.WorkflowManager().extract_workflow_shape(self._workflow_name)
            logger.info("Workflow shape: %s", workflow_shape)

            self._create_run_input = self._gather_deadline_cloud_start_flow_input(workflow_shape)
            self._deadline_cloud_start_flow_node_commands = self._get_deadline_cloud_start_flow_node_commands(
                self._unique_parameter_uuid_to_values
            )

            # Package the workflow
            package_path = self._package_workflow(self._workflow_name)
            logger.info("Workflow packaged to path: %s", package_path)

            # Publish the workflow to AWS Deadline Cloud
            job_attachment_settings, manifests = self._process_job_attachments(package_path)
            logger.info("Workflow '%s' published successfully to AWS Deadline Cloud", self._workflow_name)

            # Generate an executor workflow that can invoke the published structure
            executor_workflow_path = self._generate_executor_workflow(
                relative_dir_path=package_path,
                models_dir_path=self._resolve_path(self._get_huggingface_cache_dir()),
                attachments=manifests,
                job_attachment_settings=job_attachment_settings,
                workflow_shape=workflow_shape,
            )

            return PublishWorkflowResultSuccess(
                published_workflow_file_path=str(executor_workflow_path),
                result_details=f"Workflow '{self._workflow_name}' published successfully.",
            )
        except (ValueError, RuntimeError, ClientError, BotoCoreError) as e:
            details = f"Failed to publish workflow '{self._workflow_name}'. Error: {e}"
            logger.error(details)
            return PublishWorkflowResultFailure(
                exception=e,
                result_details=details,
            )
        except Exception as e:
            details = f"Unexpected error publishing workflow '{self._workflow_name}': {e}"
            logger.exception(details)
            return PublishWorkflowResultFailure(exception=e, result_details=details)

    def _resolve_path(self, path_to_resolve: str) -> str:
        # Use resolve() to handle mapped drives
        path = Path(path_to_resolve).resolve()
        return str(path)

    def _gather_models_for_workflow(self) -> list[str]:
        flow_manager = GriptapeNodes.FlowManager()
        get_top_level_flow_result = flow_manager.on_get_top_level_flow_request(GetTopLevelFlowRequest())
        if not isinstance(get_top_level_flow_result, GetTopLevelFlowResultSuccess):
            details = f"Failed to get top-level flow for workflow '{self._workflow_name}'."
            logger.error(details)
            raise TypeError(details)

        list_nodes_in_flow_result = flow_manager.on_list_nodes_in_flow_request(
            ListNodesInFlowRequest(flow_name=get_top_level_flow_result.flow_name)
        )
        if not isinstance(list_nodes_in_flow_result, ListNodesInFlowResultSuccess):
            details = f"Failed to list nodes in flow '{get_top_level_flow_result.flow_name}'."
            logger.error(details)
            raise TypeError(details)

        node_names = list_nodes_in_flow_result.node_names
        huggingface_repo_names = self._get_huggingface_repo_names()
        models: list[str] = []
        for node_name in node_names:
            models.extend(self._get_model_parameters_for_node(node_name, huggingface_repo_names))

        return models

    def _get_model_parameters_for_node(self, node_name: str, huggingface_repo_names: list[str]) -> list[str]:
        models: list[str] = []

        node_manager = GriptapeNodes.NodeManager()

        object_manager = GriptapeNodes.ObjectManager()
        node = object_manager.get_object_by_name(node_name)
        if node is None:
            details = f"Node '{node_name}' not found."
            logger.error(details)
            raise ValueError(details)

        if isinstance(node, BaseNode):
            parameters = node.parameters
            for param in parameters:
                get_param_value_result = node_manager.on_get_parameter_value_request(
                    GetParameterValueRequest(parameter_name=param.name, node_name=node_name)
                )
                if not isinstance(get_param_value_result, GetParameterValueResultSuccess):
                    details = f"Failed to get parameter value for '{param.name}' in node '{node_name}'."
                    logger.error(details)
                    raise TypeError(details)
                trimmed_value = str(get_param_value_result.value).split(" ")[0]
                if trimmed_value in huggingface_repo_names:
                    models.append(trimmed_value)

        return models

    def _validate_workflow(self, workflow_name: str) -> Workflow:
        """Validate the workflow before publishing."""
        workflow = self._ensure_workflow_exists(workflow_name)

        min_supported_version = Version.from_string("0.7.0")
        if workflow.metadata.schema_version is not None:
            workflow_version = Version.from_string(workflow.metadata.schema_version)
            if (
                workflow_version is not None
                and min_supported_version is not None
                and workflow_version < min_supported_version
                and self.execute_on_publish
            ):
                details = f"Workflow '{workflow_name}' has an unsupported schema version for executing on publish: {workflow.metadata.schema_version}. Minimum supported version for {LIBRARY_NAME} is {min_supported_version}. Please re-save the workflow and ensure it has a compatible schema version."
                logger.error(details)
                raise ValueError(details)
        return workflow

    def _ensure_workflow_exists(self, workflow_name: str) -> Workflow:
        """Ensure the workflow file exists in the expected location."""
        workflow = self._get_or_save_workflow(workflow_name)
        self._ensure_workflow_file_saved(workflow_name, workflow)
        return workflow

    def _get_or_save_workflow(self, workflow_name: str) -> Workflow:
        """Get workflow from registry or save it if not found."""
        try:
            return WorkflowRegistry.get_workflow_by_name(workflow_name)
        except KeyError as e:
            details = f"Workflow '{workflow_name}' not found in registry. Saving workflow."
            logger.info(details)
            result = GriptapeNodes.handle_request(
                SaveWorkflowRequest(
                    file_name=workflow_name,
                    pickle_control_flow_result=self.pickle_control_flow_result,
                )
            )
            if not isinstance(result, SaveWorkflowResultSuccess):
                details = f"Failed to save workflow '{workflow_name}' to registry."
                logger.error(details)
                raise TypeError(details) from e

            # Try again after saving
            try:
                return WorkflowRegistry.get_workflow_by_name(workflow_name)
            except KeyError as e:
                details = f"Workflow '{workflow_name}' still not found after save attempt."
                logger.error(details)
                raise ValueError(details) from e

    def _gather_deadline_cloud_start_flow_input(self, workflow_shape: dict[str, Any]) -> dict[str, Any]:
        """Extracts the Deadline Cloud Start Flow input parameters from the workflow."""
        workflow_input: dict[str, Any] = {"Deadline Cloud Start Flow": {}}

        node_manager = GriptapeNodes.NodeManager()

        # Gather input parameters from the workflow shape
        for node_name, params in workflow_shape.get("input", {}).items():
            for param_name in params:
                request = GetParameterValueRequest(
                    node_name=node_name,
                    parameter_name=param_name,
                )
                result = node_manager.on_get_parameter_value_request(request=request)
                if isinstance(result, GetParameterValueResultSuccess):
                    workflow_input["Deadline Cloud Start Flow"][param_name] = result.value

        return workflow_input

    def _ensure_workflow_file_saved(self, workflow_name: str, workflow: Workflow) -> None:
        """Ensure the workflow file exists on disk."""
        full_workflow_file_path = Path(WorkflowRegistry.get_complete_file_path(workflow.file_path))
        if not full_workflow_file_path.exists():
            details = f"Workflow file '{full_workflow_file_path}' does not exist. Saving workflow file."
            logger.info(details)
            result = GriptapeNodes.handle_request(
                SaveWorkflowRequest(
                    file_name=workflow_name,
                    pickle_control_flow_result=self.pickle_control_flow_result,
                )
            )
            if not isinstance(result, SaveWorkflowResultSuccess):
                details = f"Failed to save workflow '{workflow_name}' to file system."
                logger.error(details)
                raise ValueError(details)

            # Verify file was created
            if not full_workflow_file_path.exists():
                details = f"Workflow file '{full_workflow_file_path}' still does not exist after save attempt."
                logger.error(details)
                raise ValueError(details)

    @classmethod
    def upload_paths_as_job_attachments(  # noqa: PLR0913
        cls,
        input_paths: list[str],
        output_paths: list[str],
        farm_id: str,
        queue_id: str,
        storage_profile: StorageProfile | None,
        job_attachment_settings: JobAttachmentS3Settings,
        queue_session: Session,
    ) -> Attachments:
        """Upload specified paths as job attachments and return the attachments."""
        try:
            logger.info("Uploading %d input paths as job attachments", len(input_paths))

            # Set up asset manager and hash cache
            cache_directory = get_cache_directory()

            s3_asset_manager = S3AssetManager(
                farm_id=farm_id,
                queue_id=queue_id,
                job_attachment_settings=job_attachment_settings,
                session=queue_session,
                asset_uploader=S3AssetUploader(
                    session=queue_session,
                ),
            )

            logger.debug("Found %d input files to upload", len(input_paths))

            upload_group = s3_asset_manager.prepare_paths_for_upload(
                input_paths=input_paths, output_paths=output_paths, referenced_paths=[], storage_profile=storage_profile
            )

            # Hash assets and create manifests following GitHub example pattern
            logger.info(
                "Hashing assets and creating manifests for %d files (%d bytes)",
                upload_group.total_input_files,
                upload_group.total_input_bytes,
            )
            (_, manifests) = s3_asset_manager.hash_assets_and_create_manifest(
                upload_group.asset_groups,
                upload_group.total_input_files,
                upload_group.total_input_bytes,
                cache_directory,
            )

            def on_uploading_assets(summary: Any) -> bool:
                logger.info("Uploading assets: %s", summary)
                return True

            # Upload assets
            logger.info("Uploading %d manifests to S3", len(manifests))
            (upload_summary, attachments) = s3_asset_manager.upload_assets(
                manifests=manifests,
                s3_check_cache_dir=cache_directory,
                on_uploading_assets=on_uploading_assets,
            )

            logger.info("Upload completed: %s", upload_summary)
            return attachments  # noqa: TRY300

        except (ClientError, BotoCoreError) as e:
            details = f"AWS API error uploading job attachments: {e}"
            logger.error(details)
            raise RuntimeError(details) from e
        except OSError as e:
            details = f"File system error uploading job attachments: {e}"
            logger.error(details)
            raise RuntimeError(details) from e
        except Exception as e:
            details = f"Unexpected error uploading job attachments: {e}"
            logger.exception(details)
            raise RuntimeError(details) from e

    def _get_huggingface_cache_dir(self) -> str:
        """Get the top-level HuggingFace cache directory path."""
        return HF_HUB_CACHE

    def _get_huggingface_repo_names(self) -> list[str]:
        """Get the names of HuggingFace repositories from the huggingface_hub cache directory."""
        try:
            from huggingface_hub import scan_cache_dir

            cache_info = scan_cache_dir()
            return [repo.repo_id for repo in cache_info.repos]

        except Exception as e:
            logger.warning("Failed to get HuggingFace repo names: %s", e)
            return []

    def _get_model_paths(self, model_names: list[str]) -> list[str]:
        """Get stringified paths to model files for specific HuggingFace repositories from cache."""
        try:
            from huggingface_hub import scan_cache_dir

            if not model_names:
                logger.info("No model names provided, returning empty list")
                return []

            cache_info = scan_cache_dir()
            model_paths: list[str] = []

            # Filter repos by the requested model names
            for repo in cache_info.repos:
                if repo.repo_id in model_names:
                    # Get all file paths for this repo
                    for revision in repo.revisions:
                        for file in revision.files:
                            file_path = Path(file.file_path)
                            if (
                                file_path.exists()
                                and not file_path.is_dir()
                                and "__pycache__" not in str(file_path)
                                and ".venv" not in str(file_path)
                            ):
                                model_paths.append(str(file_path))

            # Create dummy file in HF_HUB_CACHE path to ensure cache root directory syncs to deadline
            dummy_file_path = (Path(self._get_huggingface_cache_dir()) / "dummy.txt").resolve()
            dummy_file_path.write_text("This is a dummy file for path remapping.")
            model_paths.append(str(dummy_file_path))

            logger.info("Found %d model files for %d requested repositories", len(model_paths), len(model_names))

        except Exception as e:
            logger.warning("Failed to get model paths for repositories %s: %s", model_names, e)
            return []

        else:
            return model_paths

    def _process_job_attachments(self, package_path: str) -> tuple[JobAttachmentS3Settings, Attachments]:
        """Process job attachments following the official Deadline Cloud pattern."""
        try:
            logger.info("Processing job attachments for: %s", package_path)

            logger.debug("Package path exists: %s", Path(package_path).exists())
            logger.debug("Session region: %s", self._session.region_name)
            logger.debug("Session profile: %s", getattr(self._session, "profile_name", "default"))

            # Get configuration
            farm_id = self._get_config_value(
                DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "farm_id", default=get_setting_default("defaults.farm_id")
            )
            queue_id = self._get_config_value(
                DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "queue_id", default=get_setting_default("defaults.queue_id")
            )
            storage_profile_id = self._get_config_value(
                DEADLINE_CLOUD_LIBRARY_CONFIG_KEY,
                "storage_profile_id",
                default=get_setting_default("settings.storage_profile_id"),
            )

            if self._create_run_input.get("Deadline Cloud Start Flow") is not None:
                start_flow_input = self._create_run_input["Deadline Cloud Start Flow"]
                if "farm_id" in start_flow_input:
                    farm_id = start_flow_input["farm_id"]
                if "queue_id" in start_flow_input:
                    queue_id = start_flow_input["queue_id"]
                if "storage_profile_id" in start_flow_input:
                    storage_profile_id = start_flow_input["storage_profile_id"]

            logger.info("Using farm_id: %s, queue_id: %s", farm_id, queue_id)
            enable_models_as_attachments = self._get_config_value(
                DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "enable_models_as_attachments", default=True
            )

            # Initialize Deadline client
            deadline_client = self._get_client()

            # Get queue information for job attachment settings
            queue_response = deadline_client.get_queue(farmId=farm_id, queueId=queue_id)
            job_attachment_settings = JobAttachmentS3Settings(**queue_response["jobAttachmentSettings"])

            queue_session = get_queue_user_boto3_session(
                deadline_client,
                None,
                farm_id,
                queue_id,
            )
            queue_session._session.set_config_variable("region", self._session.region_name)

            # Set up asset manager and hash cache
            job_bundle_path = Path(package_path)
            assets_dir = job_bundle_path / "assets"

            # Prepare paths for upload - expand directory to individual files
            input_paths = []
            if assets_dir.is_dir():
                input_paths.extend(
                    [
                        str(file_path)
                        for file_path in assets_dir.glob("**/*")
                        if not file_path.is_dir()
                        and file_path.exists()
                        and "__pycache__" not in str(file_path)
                        and ".venv" not in str(file_path)
                    ]
                )

            # Gather model files for use as input paths
            if enable_models_as_attachments:
                model_names = self._gather_models_for_workflow()
                model_paths = self._get_model_paths(model_names)
                input_paths.extend(model_paths)

            storage_profile: StorageProfile | None = self._get_storage_profile_for_queue(
                farm_id, queue_id, storage_profile_id
            )

            # Use the classmethod to handle the actual upload
            attachments = self.upload_paths_as_job_attachments(
                input_paths=input_paths,
                output_paths=[str(job_bundle_path / "output")],
                farm_id=farm_id,
                queue_id=queue_id,
                storage_profile=storage_profile,
                job_attachment_settings=job_attachment_settings,
                queue_session=queue_session,
            )

        except (ClientError, BotoCoreError) as e:
            details = f"AWS API error processing job attachments: {e}"
            logger.error(details)
            raise RuntimeError(details) from e
        except OSError as e:
            details = f"File system error processing job attachments: {e}"
            logger.error(details)
            raise RuntimeError(details) from e
        except Exception as e:
            details = f"Unexpected error processing job attachments: {e}"
            logger.exception(details)
            raise RuntimeError(details) from e

        # Return job attachment settings and manifests for job submission
        return job_attachment_settings, attachments

    def _copy_libraries_to_path_for_workflow(
        self,
        node_libraries: list[LibraryNameAndVersion],
        destination_path: Path,
        runtime_env_path: Path,
        workflow: Workflow,
    ) -> list[str]:
        """Copies the libraries to the specified path for the workflow, returning the list of library paths.

        This is used to package the workflow for publishing.
        """
        library_paths: list[str] = []

        for library_ref in node_libraries:
            library = GriptapeNodes.LibraryManager().get_library_info_by_library_name(library_ref.library_name)

            if library is None:
                details = f"Attempted to publish workflow '{workflow.metadata.name}', but failed gathering library info for library '{library_ref.library_name}'."
                logger.error(details)
                raise ValueError(details)

            library_data = LibraryRegistry.get_library(library_ref.library_name).get_library_data()

            if library.library_path.endswith(".json"):
                library_path = Path(library.library_path)
                absolute_library_path = library_path.resolve()
                abs_paths = [absolute_library_path]
                for node in library_data.nodes:
                    p = (library_path.parent / Path(node.file_path)).resolve()
                    abs_paths.append(p)
                common_root = Path(os.path.commonpath([str(p) for p in abs_paths]))
                dest = destination_path / common_root.name
                shutil.copytree(
                    common_root, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".venv", "__pycache__")
                )
                library_path_relative_to_common_root = absolute_library_path.relative_to(common_root)
                library_paths.append(
                    (runtime_env_path / common_root.name / library_path_relative_to_common_root).as_posix()
                )
            else:
                library_paths.append(library.library_path)

        return library_paths

    def __get_install_source(self) -> tuple[Literal["git", "file", "pypi"], str | None]:
        """Determines the install source of the Griptape Nodes package.

        Returns:
            tuple: A tuple containing the install source and commit ID (if applicable).
        """
        dist = importlib.metadata.distribution("griptape_nodes")
        direct_url_text = dist.read_text("direct_url.json")
        # installing from pypi doesn't have a direct_url.json file
        if direct_url_text is None:
            logger.debug("No direct_url.json file found, assuming pypi install")
            return "pypi", None

        direct_url_info = json.loads(direct_url_text)
        url = direct_url_info.get("url")
        if url.startswith("file://"):
            try:
                pkg_dir = Path(str(dist.locate_file(""))).resolve()
                git_root = next(p for p in (pkg_dir, *pkg_dir.parents) if (p / ".git").is_dir())
                commit = (
                    subprocess.check_output(
                        ["git", "rev-parse", "--short", "HEAD"],  # noqa: S607
                        cwd=git_root,
                        stderr=subprocess.DEVNULL,
                    )
                    .decode()
                    .strip()
                )
            except (StopIteration, subprocess.CalledProcessError):
                logger.debug("File URL but no git repo → file")
                return "file", None
            else:
                logger.debug("Detected git repo at %s (commit %s)", git_root, commit)
                return "git", commit
        if "vcs_info" in direct_url_info:
            logger.debug("Detected git repo at %s", url)
            return "git", direct_url_info["vcs_info"].get("commit_id")[:7]
        # Fall back to pypi if no other source is found
        logger.debug("Failed to detect install source, assuming pypi")
        return "pypi", None

    def _get_merged_env_file_mapping(self, workspace_env_file_path: Path) -> dict[str, Any]:
        """Merges the secrets from the workspace env file with the secrets from the GriptapeNodes SecretsManager.

        This is used to create a single .env file for the workflow. We can gather all secrets explicitly defined in the .env file
        and by the settings/SecretsManager, but we will not gather all secrets from the OS env for the purpose of publishing.
        """
        env_file_dict: dict[str, Any] = {}
        if workspace_env_file_path.exists():
            env_file = DotEnv(workspace_env_file_path)
            env_file_dict = env_file.dict()

        get_all_secrets_request = GetAllSecretValuesRequest()
        get_all_secrets_result = GriptapeNodes.handle_request(request=get_all_secrets_request)
        if not isinstance(get_all_secrets_result, GetAllSecretValuesResultSuccess):
            details = "Failed to get all secret values."
            logger.error(details)
            raise TypeError(details)

        secret_values = get_all_secrets_result.values
        for secret_name, secret_value in secret_values.items():
            if secret_name not in env_file_dict:
                env_file_dict[secret_name] = secret_value

        return env_file_dict

    def _write_env_file(self, env_file_path: Path, env_file_dict: dict[str, Any]) -> None:
        env_file_path.touch(exist_ok=True)
        for key, val in env_file_dict.items():
            set_key(env_file_path, key, str(val))

    def _get_engine_version_for_workflow(self, workflow: Workflow) -> str:
        # Get engine version for dependencies
        engine_version_request = GetEngineVersionRequest()
        engine_version_result = GriptapeNodes.handle_request(request=engine_version_request)
        if not engine_version_result.succeeded():
            details = f"Failed to get engine version for workflow '{workflow.metadata.name}'"
            logger.error(details)
            raise ValueError(details)
        engine_version_success = cast("GetEngineVersionResultSuccess", engine_version_result)
        return f"v{engine_version_success.major}.{engine_version_success.minor}.{engine_version_success.patch}"

    def _package_workflow(self, workflow_name: str) -> str:
        """Package workflow as a Deadline Cloud job bundle with Open Job Description template."""
        config_manager = GriptapeNodes.get_instance()._config_manager
        secrets_manager = GriptapeNodes.get_instance()._secrets_manager
        workflow = WorkflowRegistry.get_workflow_by_name(workflow_name)

        # Get engine version for dependencies
        engine_version = self._get_engine_version_for_workflow(workflow)

        # Create temporary directory for packaging
        temp_dir = Path(tempfile.mkdtemp(prefix=f"{workflow_name}_deadline_bundle_"))
        job_bundle_dir = temp_dir
        assets_dir = job_bundle_dir / "assets"

        # Create bundle directory structure
        assets_dir.mkdir(parents=True)

        try:
            local_publish_path = Path(__file__).parent

            # 1. Copy workflow and dependencies to assets
            full_workflow_file_path = WorkflowRegistry.get_complete_file_path(workflow.file_path)
            shutil.copyfile(full_workflow_file_path, assets_dir / "workflow.py")

            init_file_path = local_publish_path / "__init__.py"
            shutil.copyfile(init_file_path, assets_dir / "__init__.py")

            deadline_workflow_executor_file_path = local_publish_path / "deadline_cloud_workflow_executor.py"
            shutil.copyfile(deadline_workflow_executor_file_path, assets_dir / "deadline_cloud_workflow_executor.py")

            # 2. Copy libraries
            library_paths = self._copy_libraries_to_path_for_workflow(
                node_libraries=workflow.metadata.node_libraries_referenced,
                destination_path=assets_dir / "libraries",
                runtime_env_path=Path("{{Param.LocationToRemap}}/assets/libraries"),
                workflow=workflow,
            )

            # 3. Create configuration
            config = config_manager.user_config.copy()
            config["workspace_directory"] = "."
            config["app_events"] = {
                "on_app_initialization_complete": {
                    "workflows_to_register": [],
                    "libraries_to_register": library_paths,
                }
            }

            with (assets_dir / "griptape_nodes_config.json").open("w", encoding="utf-8") as config_file:
                json.dump(config, config_file, indent=2)

            # 4. Create environment file
            env_file_mapping = self._get_merged_env_file_mapping(secrets_manager.workspace_env_path)
            self._write_env_file(assets_dir / ".env", env_file_mapping)

            # 5. Create requirements.txt
            source, commit_id = self.__get_install_source()
            if source == "git" and commit_id is not None:
                engine_version = commit_id

            with (assets_dir / "requirements.txt").open("w", encoding="utf-8") as req_file:
                req_file.write(
                    f"griptape-nodes @ git+https://github.com/griptape-ai/griptape-nodes.git@{engine_version}\n"
                )

            # 6. Generate Job Template
            self._job_template = DeadlineCloudJobTemplateGenerator.generate_job_template(
                job_bundle_dir, workflow_name, library_paths, self.pickle_control_flow_result
            )

            logger.info("Job bundle created at: %s", job_bundle_dir)
            return str(job_bundle_dir)

        except OSError as e:
            details = f"File system error packaging workflow '{workflow_name}': {e}"
            logger.error(details)
            raise RuntimeError(details) from e
        except (ValueError, TypeError) as e:
            details = f"Configuration error packaging workflow '{workflow_name}': {e}"
            logger.error(details)
            raise
        except Exception as e:
            details = f"Unexpected error packaging workflow '{workflow_name}': {e}"
            logger.exception(details)
            raise RuntimeError(details) from e

    def _get_deadline_cloud_start_flow_node_commands(
        self, unique_parameter_uuid_to_values: dict
    ) -> SerializeNodeToCommandsResultSuccess | None:
        flow_manager = GriptapeNodes.FlowManager()
        result = flow_manager.on_get_top_level_flow_request(GetTopLevelFlowRequest())
        if result.failed():
            details = f"Workflow '{self._workflow_name}' does not have a top-level flow."
            raise ValueError(details)
        flow_name = cast("GetTopLevelFlowResultSuccess", result).flow_name
        if flow_name is None:
            details = f"Workflow '{self._workflow_name}' does not have a top-level flow."
            raise ValueError(details)

        control_flow = flow_manager.get_flow_by_name(flow_name)
        nodes = control_flow.nodes

        dc_start_node: DeadlineCloudStartFlow | None = None

        for node in nodes.values():
            if node.metadata["library"] == LIBRARY_NAME and isinstance(node, StartNode):
                dc_start_node = cast("DeadlineCloudStartFlow", node)

        if dc_start_node is None:
            logger.warning("No DeadlineCloudStartFlow node found.")
            return None

        serialize_node_to_commands_request = SerializeNodeToCommandsRequest(
            node_name=dc_start_node.name,
            unique_parameter_uuid_to_values=unique_parameter_uuid_to_values,
        )
        serialize_node_to_commands_result = GriptapeNodes.handle_request(serialize_node_to_commands_request)
        if not isinstance(serialize_node_to_commands_result, SerializeNodeToCommandsResultSuccess):
            details = f"Failed to serialize node '{dc_start_node.name}' to commands."
            logger.error(details)
            raise TypeError(details)

        logger.debug("Serialized DeadlineCloudStartFlow node to commands successfully.")
        logger.debug("Node commands: %s", serialize_node_to_commands_result.serialized_node_commands)
        logger.debug("Node parameters: %s", serialize_node_to_commands_result.set_parameter_value_commands)
        return serialize_node_to_commands_result

    def _generate_executor_workflow(
        self,
        relative_dir_path: str,
        models_dir_path: str,
        attachments: Attachments,
        job_attachment_settings: JobAttachmentS3Settings,
        workflow_shape: dict[str, Any],
    ) -> Path:
        """Generate a new workflow file that can execute the published workflow.

        This creates a simple workflow with StartNode -> DeadlineCloudPublishedWorkflow -> EndNode
        that can invoke the published workflow in Deadline Cloud.

        Args:
            relative_dir_path: The relative directory path to the packaged workflow bundle.
            models_dir_path: The directory path for HuggingFace model cache location.
            attachments: The job attachments to be used in the executor workflow.
            job_attachment_settings: The job attachment S3 settings for Deadline Cloud.
            workflow_shape: The input/output shape of the original workflow.
        """
        # Use WorkflowBuilder to generate the executor workflow
        libraries: list[LibraryManager.LibraryInfo] = []
        if nodes_library := GriptapeNodes.LibraryManager().get_library_info_by_library_name("Griptape Nodes Library"):
            libraries.append(nodes_library)
        else:
            details = "Griptape Nodes Library is not available. Cannot generate executor workflow."
            logger.error(details)
            raise ValueError(details)
        if deadline_cloud_library := GriptapeNodes.LibraryManager().get_library_info_by_library_name(
            "AWS Deadline Cloud Library"
        ):
            libraries.append(deadline_cloud_library)
        else:
            details = "AWS Deadline Cloud Library is not available. Cannot generate executor workflow."
            logger.error(details)
            raise ValueError(details)
        library_paths = [library.library_path for library in libraries if library.library_path is not None]
        builder = DeadlineCloudWorkflowBuilder(
            workflow_builder_input=DeadlineCloudWorkflowBuilderInput(
                attachments=attachments,
                job_attachment_settings=job_attachment_settings,
                job_template=self._job_template,
                relative_dir_path=relative_dir_path,
                models_dir_path=models_dir_path,
                workflow_name=self._workflow_name,
                workflow_shape=workflow_shape,
                executor_workflow_name=self._published_workflow_file_name,
                deadline_cloud_start_flow_input=self._create_run_input["Deadline Cloud Start Flow"],
                deadline_cloud_start_flow_node_commands=self._deadline_cloud_start_flow_node_commands,
                unique_parameter_uuid_to_values=self._unique_parameter_uuid_to_values,
                libraries=library_paths,
                pickle_control_flow_result=self.pickle_control_flow_result,
            )
        )
        return builder.generate_executor_workflow()
