"""WorkflowBuilder for generating a Griptape Nodes workflow that can invoke a published workflow in the form of a Deadline Cloud job.

This module provides simple script generation for creating workflows that follow the pattern:
StartNode -> PublishedWorkflow -> EndNode
"""

import logging
import subprocess
import sys
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from deadline.job_attachments.models import Attachments, JobAttachmentS3Settings
from griptape_nodes.retained_mode.events.node_events import (
    SerializeNodeToCommandsResultSuccess,
)
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes
from publish import LIBRARY_NAME
from publish.deadline_cloud_end_flow import DeadlineCloudEndFlow
from publish.deadline_cloud_published_workflow import DeadlineCloudPublishedWorkflow
from publish.deadline_cloud_start_flow import DeadlineCloudStartFlow

logger = logging.getLogger(__name__)


@dataclass
class DeadlineCloudWorkflowBuilderInput:
    attachments: Attachments
    job_attachment_settings: JobAttachmentS3Settings
    job_template: dict[str, Any]
    relative_dir_path: str
    models_dir_path: str
    workflow_name: str
    workflow_shape: dict[str, Any]
    executor_workflow_name: str
    deadline_cloud_start_flow_input: dict[str, Any]
    deadline_cloud_start_flow_node_commands: SerializeNodeToCommandsResultSuccess | None = None
    unique_parameter_uuid_to_values: dict = field(default_factory=dict)
    libraries: list[str] = field(default_factory=list)
    pickle_control_flow_result: bool = False


class DeadlineCloudWorkflowBuilder:
    """Builder class for generating executor workflows using simple script generation."""

    def __init__(
        self,
        workflow_builder_input: DeadlineCloudWorkflowBuilderInput,
    ) -> None:
        """Initialize the WorkflowBuilder.

        Args:
            workflow_builder_input: Input configuration containing all necessary parameters.
        """
        self.workflow_builder_input = workflow_builder_input

    def generate_executor_workflow(
        self,
    ) -> Path:
        """Generate an executor workflow that can invoke the published Deadline Cloud job."""
        # Generate a simple workflow creation script using PublishedWorkflow node
        workflow_script = self._build_simple_workflow_script(
            self.workflow_builder_input.job_template,
            self.workflow_builder_input.workflow_shape,
            self.workflow_builder_input.libraries,
        )

        # Execute the script in a subprocess to create the workflow
        self._execute_workflow_script(workflow_script)

        # Verify the workflow was created successfully
        executor_workflow_path = GriptapeNodes.ConfigManager().workspace_path / (
            self.workflow_builder_input.executor_workflow_name + ".py"
        )
        if not executor_workflow_path.exists():
            error_msg = (
                f"Executor workflow {self.workflow_builder_input.executor_workflow_name} was not created successfully."
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        return executor_workflow_path

    def _build_library_registration_script(self, libraries: list[str]) -> str:
        """Build a script to register libraries for the workflow.

        Args:
            libraries: List of library paths to register

        Returns:
            Complete Python script as string
        """
        if not libraries:
            return ""

        # Build the library registration script
        script = ""

        for i, lib in enumerate(libraries):
            if lib.endswith(".json"):
                script += f"""
    request_{i!s} = GriptapeNodes.handle_request(RegisterLibraryFromFileRequest(file_path={lib!r}))
"""
            else:
                script += f"""
    request_{i!s} = GriptapeNodes.handle_request(RegisterLibraryFromRequirementSpecifierRequest(requirement_specifier={lib!r}))
"""
        return script

    def _build_simple_workflow_script(  # noqa: C901, PLR0912, PLR0915
        self, job_template: dict, workflow_shape: dict[str, Any], libraries: list[str]
    ) -> str:
        """Build a simple workflow creation script using PublishedWorkflow node.

        Args:
            job_template: The job template to use for the Deadline Cloud job
            workflow_shape: Input/output parameter structure
            libraries: List of libraries needed for the workflow

        Returns:
            Complete Python script as string
        """
        # Get parameter information directly from workflow_shape
        input_params = []
        if "input" in workflow_shape:
            for node_params in workflow_shape["input"].values():
                if isinstance(node_params, dict):
                    input_params.extend(node_params.values())

        output_params = []
        if "output" in workflow_shape:
            for node_params in workflow_shape["output"].values():
                if isinstance(node_params, dict):
                    output_params.extend(node_params.values())

        # Build the workflow generation script
        script = f'''
"""
Generated executor workflow for invoking a Deadline Cloud job to run a workflow.
"""

from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes
from griptape_nodes.retained_mode.events.flow_events import CreateFlowRequest
from griptape_nodes.retained_mode.events.node_events import CreateNodeRequest
from griptape_nodes.retained_mode.events.library_events import (
    RegisterLibraryFromFileRequest,
    RegisterLibraryFromRequirementSpecifierRequest,
)
from griptape_nodes.retained_mode.events.parameter_events import AddParameterToNodeRequest, SetParameterValueRequest
from griptape_nodes.retained_mode.events.connection_events import CreateConnectionRequest
from griptape_nodes.retained_mode.events.workflow_events import SaveWorkflowRequest

def main():
    {self._build_library_registration_script(libraries)}

    context_manager = GriptapeNodes.ContextManager()
    if not context_manager.has_current_workflow():
        context_manager.push_workflow(workflow_name="{self.workflow_builder_input.executor_workflow_name}")

    # Create the main flow
    flow_response = GriptapeNodes.handle_request(CreateFlowRequest(parent_flow_name=None))
    flow_name = flow_response.flow_name

    with GriptapeNodes.ContextManager().flow(flow_name):
        # Create StartNode
        start_node_response = GriptapeNodes.handle_request(CreateNodeRequest(
            node_type="{DeadlineCloudStartFlow.__name__}",
            specific_library_name="{LIBRARY_NAME}",
            node_name="Deadline Cloud Start Flow",
            initial_setup=True
        ))
        start_node_name = start_node_response.node_name

        # Create DeadlineCloudPublishedWorkflow node
        published_wf_response = GriptapeNodes.handle_request(CreateNodeRequest(
            node_type="{DeadlineCloudPublishedWorkflow.__name__}",
            specific_library_name="{LIBRARY_NAME}",
            node_name="AWS Deadline Cloud Published Workflow",
            metadata={{
                "workflow_shape": {workflow_shape!r},
                "job_template": {job_template!r},
                "job_attachment_settings": {asdict(self.workflow_builder_input.job_attachment_settings)!r},
                "attachments": {self.workflow_builder_input.attachments.to_dict()!r},
                "relative_dir_path": {self.workflow_builder_input.relative_dir_path!r},
                "models_dir_path": {self.workflow_builder_input.models_dir_path!r},
            }},
            initial_setup=True
        ))
        published_wf_name = published_wf_response.node_name

        # Create EndNode
        end_node_response = GriptapeNodes.handle_request(CreateNodeRequest(
            node_type="{DeadlineCloudEndFlow.__name__}",
            specific_library_name="{LIBRARY_NAME}",
            node_name="Deadline Cloud End Flow",
            initial_setup=True
        ))
        end_node_name = end_node_response.node_name

        # Configure StartNode parameters
        with GriptapeNodes.ContextManager().node(start_node_name):'''

        non_deadline_params = [
            param
            for param in input_params
            if param["name"] not in DeadlineCloudPublishedWorkflow.get_default_node_parameter_names()
        ]

        if len(non_deadline_params) == 0:
            script += """
            pass
        """
        else:
            # Add parameter configuration for StartNode
            for param in input_params:
                # Create a copy and remap 'name' to 'parameter_name'
                param_config = dict(param)
                param_name = param_config.pop("name")
                param_config.pop("settable", None)  # Remove 'settable' if it exists
                param_config["parameter_name"] = param_name
                if param_name not in DeadlineCloudPublishedWorkflow.get_default_node_parameter_names():
                    # Do not double add job submission parameters
                    script += f"""
            GriptapeNodes.handle_request(AddParameterToNodeRequest(
                **{param_config},
                mode_allowed_input=False,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True
            ))"""

        script += """

        # Configure DeadlineCloudPublishedWorkflow parameters
        with GriptapeNodes.ContextManager().node(published_wf_name):"""

        if len(input_params) == 0:
            script += """
            pass
        """
        else:
            # Add input parameter configuration for DeadlineCloudPublishedWorkflow
            for param in input_params:
                # Create a copy and remap 'name' to 'parameter_name'
                param_config = dict(param)
                param_name = param_config.pop("name")
                param_config["parameter_name"] = param_name
                param_config.pop("settable", None)  # Remove 'settable' if it exists
                if param_name not in DeadlineCloudPublishedWorkflow.get_default_node_parameter_names():
                    script += f"""
            GriptapeNodes.handle_request(AddParameterToNodeRequest(
                **{param_config},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=False,
                initial_setup=True
            ))"""

            # Add output parameter configuration for DeadlineCloudPublishedWorkflow
            for param in output_params:
                # Create a copy and remap 'name' to 'parameter_name'
                param_config = dict(param)
                param_name = param_config.pop("name")
                param_config["parameter_name"] = param_name
                param_config.pop("settable", None)  # Remove 'settable' if it exists
                if param_name not in DeadlineCloudPublishedWorkflow.get_default_node_parameter_names():
                    script += f"""
            GriptapeNodes.handle_request(AddParameterToNodeRequest(
                **{param_config},
                mode_allowed_input=False,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True
            ))"""

        script += """

        # Configure EndNode parameters
        with GriptapeNodes.ContextManager().node(end_node_name):"""

        if len(non_deadline_params) == 0:
            script += """
            pass
        """
        else:
            # Add parameter configuration for EndNode
            for param in output_params:
                # Create a copy and remap 'name' to 'parameter_name'
                param_config = dict(param)
                param_name = param_config.pop("name")
                param_config["parameter_name"] = param_name
                param_config.pop("settable", None)  # Remove 'settable' if it exists
                if param_name not in DeadlineCloudEndFlow.get_default_node_parameter_names():
                    script += f"""
            GriptapeNodes.handle_request(AddParameterToNodeRequest(
                **{param_config},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=False,
                initial_setup=True
            ))"""

        script += """

    # Create connections between StartNode and DeadlineCloudPublishedWorkflow"""

        # Add connections for submission parameters
        for param_name in DeadlineCloudPublishedWorkflow.get_default_node_parameter_names():
            script += f"""
    GriptapeNodes.handle_request(CreateConnectionRequest(
        source_node_name=start_node_name,
        source_parameter_name="{param_name}",
        target_node_name=published_wf_name,
        target_parameter_name="{param_name}",
        initial_setup=True
    ))"""

        # Add connections for each input parameter
        for param in input_params:
            script += f"""
    GriptapeNodes.handle_request(CreateConnectionRequest(
        source_node_name=start_node_name,
        source_parameter_name="{param["name"]}",
        target_node_name=published_wf_name,
        target_parameter_name="{param["name"]}",
        initial_setup=True
    ))"""

        script += """

    # Create connections between DeadlineCloudPublishedWorkflow and EndNode"""

        # Add connections for each output parameter
        for param in output_params:
            script += f"""
    GriptapeNodes.handle_request(CreateConnectionRequest(
        source_node_name=published_wf_name,
        source_parameter_name="{param["name"]}",
        target_node_name=end_node_name,
        target_parameter_name="{param["name"]}",
        initial_setup=True
    ))"""

        control_flow: dict = {"exec_out": "exec_in", "failure": "failed"}
        for key, val in control_flow.items():
            script += f"""
    GriptapeNodes.handle_request(CreateConnectionRequest(
        source_node_name=published_wf_name,
        source_parameter_name="{key}",
        target_node_name=end_node_name,
        target_parameter_name="{val}",
        initial_setup=True
    ))"""

        script += """

    # Set parameter values for Deadline Cloud Start Flow"""

        if self.workflow_builder_input.deadline_cloud_start_flow_node_commands is not None:
            script += f"""
    unique_values_dict = {self.workflow_builder_input.unique_parameter_uuid_to_values}
    """
            items = self.workflow_builder_input.deadline_cloud_start_flow_input
            # This ensures all job submission parameters are included
            for param in DeadlineCloudPublishedWorkflow.get_default_node_parameter_names():
                if param not in items:
                    items[param] = None
            for param_name, param_value in items.items():
                for (
                    command
                ) in self.workflow_builder_input.deadline_cloud_start_flow_node_commands.set_parameter_value_commands:
                    if command.set_parameter_value_command.parameter_name == param_name:
                        script += f"""
    GriptapeNodes.handle_request(SetParameterValueRequest(
        node_name=start_node_name,
        parameter_name="{param_name}",
        value=unique_values_dict.get({command.unique_value_uuid!r}, {param_value!r}),
        initial_setup=True
    ))"""

        script += f"""

    # Save the workflow
    save_response = GriptapeNodes.handle_request(SaveWorkflowRequest(
        file_name="{self.workflow_builder_input.executor_workflow_name}",
        pickle_control_flow_result={self.workflow_builder_input.pickle_control_flow_result}))

    if save_response.succeeded():
        print(f"Successfully created executor workflow: {self.workflow_builder_input.executor_workflow_name}")
    else:
        print(f"Failed to create executor workflow")
        exit(1)

if __name__ == "__main__":
    main()
"""

        return script

    def _execute_workflow_script(self, script: str) -> None:
        """Execute the workflow creation script in a subprocess."""
        temp_script_path = Path(__file__).parent / f"temp_executor_{uuid.uuid4().hex}.py"

        try:
            with temp_script_path.open("w", encoding="utf-8") as f:
                f.write(script)

            # Execute the script in a subprocess to isolate the GriptapeNodes state
            result = subprocess.run(  # noqa: S603
                [sys.executable, str(temp_script_path)],
                capture_output=True,
                text=True,
                cwd=temp_script_path.parent,
                timeout=300,
                check=False,
            )

            # Print subprocess output
            if result.stdout:
                logger.debug(result.stdout)
            if result.stderr:
                logger.debug(result.stderr)

            if result.returncode != 0:
                error_msg = f"Executor workflow generation failed: {result.stderr}"
                logger.error("Failed to generate executor workflow: %s", result.stderr)
                raise RuntimeError(error_msg)

            logger.info(
                "Successfully generated executor workflow: %s", self.workflow_builder_input.executor_workflow_name
            )

        finally:
            # Clean up temporary script
            if temp_script_path.exists():
                temp_script_path.unlink()
