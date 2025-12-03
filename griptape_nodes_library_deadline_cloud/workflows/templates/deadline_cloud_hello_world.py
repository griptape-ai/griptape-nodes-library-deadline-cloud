# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_hello_world"
# description = "A simple example demonstrating how a node can be tagged for execution on AWS Deadline Cloud within an existing workflow."
# schema_version = "0.13.0"
# engine_version_created_with = "0.64.1"
# node_libraries_referenced = [["Griptape Nodes Library", "0.51.1"], ["AWS Deadline Cloud Library", "0.64.1"]]
# node_types_used = [["Griptape Nodes Library", "AddTextToImage"], ["Griptape Nodes Library", "DisplayImage"], ["Griptape Nodes Library", "DisplayText"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "TextInput"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-12-01T22:51:55.676587Z
# last_modified_date = 2025-12-01T23:16:03.246140Z
#
# ///

import pickle
from griptape_nodes.node_library.library_registry import IconVariant, NodeDeprecationMetadata, NodeMetadata
from griptape_nodes.retained_mode.events.connection_events import CreateConnectionRequest
from griptape_nodes.retained_mode.events.flow_events import CreateFlowRequest
from griptape_nodes.retained_mode.events.library_events import LoadLibrariesRequest
from griptape_nodes.retained_mode.events.node_events import CreateNodeGroupRequest, CreateNodeRequest
from griptape_nodes.retained_mode.events.parameter_events import (
    AddParameterToNodeRequest,
    AlterParameterDetailsRequest,
    SetParameterValueRequest,
)
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

GriptapeNodes.handle_request(LoadLibrariesRequest())

context_manager = GriptapeNodes.ContextManager()

if not context_manager.has_current_workflow():
    context_manager.push_workflow(workflow_name="deadline_cloud_hello_world")

"""
1. We've collated all of the unique parameter values into a dictionary so that we do not have to duplicate them.
   This minimizes the size of the code, especially for large objects like serialized image files.
2. We're using a prefix so that it's clear which Flow these values are associated with.
3. The values are serialized using pickle, which is a binary format. This makes them harder to read, but makes
   them consistently save and load. It allows us to serialize complex objects like custom classes, which otherwise
   would be difficult to serialize.
"""
top_level_unique_values_dict = {
    "4af11d7d-b32a-4d75-806f-c6a421510117": pickle.loads(b"\x80\x04K\x00."),
    "cf0f8055-3131-4429-b86a-d4e3410a4a4a": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "0ca3907e-1977-4f70-9cd6-6089a935ed6d": pickle.loads(
        b"\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rHello, world!\x94."
    ),
    "9f42bf68-765d-439b-802a-506111950a11": pickle.loads(
        b'\x80\x04\x95\x85\x00\x00\x00\x00\x00\x00\x00\x8c\x81This workflow demonstrates a simple "hello world" example for confirming AWS Deadline Cloud functionality is working as expected.\x94.'
    ),
    "416d6cee-8c18-48b8-ada3-43c8655eb920": pickle.loads(
        b"\x80\x04\x95p\x00\x00\x00\x00\x00\x00\x00\x8clThis is the happy path, indicating success. Your image will appear if Deadline Cloud completes successfully.\x94."
    ),
    "4f69c241-7b5d-4e05-8f6e-9011a87a4775": pickle.loads(
        b"\x80\x04\x95\x84\x00\x00\x00\x00\x00\x00\x00\x8c\x80If execution in Deadline Cloud fails, this path will be executed. The Display Text will provide information about what occurred.\x94."
    ),
    "5c3b34ee-3ddc-4eeb-a49a-56bb5d44d9cf": pickle.loads(
        b"\x80\x04\x95\x18\x01\x00\x00\x00\x00\x00\x00X\x11\x01\x00\x00This node will be executed on Deadline Cloud.\n\nThe NodeGroup settings can be configured to specify an execution_environment of `AWS Deadline Cloud Library`, which indicates that all Nodes within the group should be packaged and shipped up to Deadline Cloud to run as a Job.\x94."
    ),
    "b7d7f771-cf61-43ee-a858-9b56e0bf996d": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "8c3a94d7-85d3-4c30-823a-93ee6638eabd": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bHello World\x94."
    ),
    "bd96fd97-d765-4e90-a03a-298212597afc": pickle.loads(
        b'\x80\x04\x95j\x00\x00\x00\x00\x00\x00\x00\x8cfA simple "hello world" example for confirming AWS Deadline Cloud functionality is working as expected.\x94.'
    ),
    "a17453a2-0bb9-49d9-af5e-351376b226d6": pickle.loads(
        b"\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rHello, world!\x94."
    ),
}

"# Create the Flow, then do work within it as context."

flow0_name = GriptapeNodes.handle_request(
    CreateFlowRequest(parent_flow_name=None, flow_name="ControlFlow_1", set_as_new_context=False, metadata={})
).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DisplayImage",
            specific_library_name="Griptape Nodes Library",
            node_name="Display Image",
            metadata={
                "position": {"x": 1945.6666666666667, "y": 337.01202725017583},
                "tempId": "placing-1764628982995-w9g86",
                "library_node_metadata": {"category": "image", "description": "Display an image"},
                "library": "Griptape Nodes Library",
                "node_type": "DisplayImage",
                "showaddparameter": False,
                "size": {"width": 699, "height": 525},
                "category": "image",
            },
            initial_setup=True,
        )
    ).node_name
    node1_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DisplayText",
            specific_library_name="Griptape Nodes Library",
            node_name="Display Text",
            metadata={
                "position": {"x": 1941.6666666666667, "y": 1156.6666666666667},
                "tempId": "placing-1764629234821-3a48sq",
                "library_node_metadata": NodeMetadata(
                    category="text",
                    description="DisplayText node",
                    display_name="Display Text",
                    tags=None,
                    icon=None,
                    color=None,
                    group="display",
                    deprecation=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "DisplayText",
                "showaddparameter": False,
                "size": {"width": 713, "height": 402},
                "category": "text",
            },
            initial_setup=True,
        )
    ).node_name
    node2_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="TextInput",
            specific_library_name="Griptape Nodes Library",
            node_name="Text Input",
            metadata={
                "position": {"x": 23.519849367752443, "y": 337.01202725017583},
                "tempId": "placing-1764629407956-5xbh8",
                "library_node_metadata": {"category": "text", "description": "TextInput node"},
                "library": "Griptape Nodes Library",
                "node_type": "TextInput",
                "showaddparameter": False,
                "size": {"width": 600, "height": 236},
                "category": "text",
            },
            initial_setup=True,
        )
    ).node_name
    node3_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Workflow Summary",
            metadata={
                "position": {"x": 23.519849367752443, "y": 86.6904695896311},
                "tempId": "placing-1764629334034-pdx54k",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "size": {"width": 600, "height": 227},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    node4_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Successful Path",
            metadata={
                "position": {"x": 1941.6666666666667, "y": 86.69046958963114},
                "tempId": "placing-1764629458611-z3mgu",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "size": {"width": 693, "height": 217},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    node5_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Unsuccessful Path",
            metadata={
                "position": {"x": 1941.6666666666667, "y": 941.0120272501758},
                "tempId": "placing-1764629487845-mzlqzi",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "size": {"width": 708, "height": 196},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    node6_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Execution Environment",
            metadata={
                "position": {"x": 749.0223191048804, "y": 76.6904695896311},
                "tempId": "placing-1764629928719-jksmwo",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "size": {"width": 1003, "height": 251},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    """# Create the Flow, then do work within it as context."""
    flow1_name = GriptapeNodes.handle_request(
        CreateFlowRequest(
            parent_flow_name=flow0_name, flow_name="NodeGroup_subflow", set_as_new_context=False, metadata={}
        )
    ).flow_name
    with GriptapeNodes.ContextManager().flow(flow1_name):
        node7_name = GriptapeNodes.handle_request(
            CreateNodeRequest(
                node_type="AddTextToImage",
                specific_library_name="Griptape Nodes Library",
                node_name="Add Text to Image",
                metadata={
                    "position": {"x": 208.4920383067995, "y": 155.01202725017583},
                    "tempId": "placing-1764628967865-yle2e",
                    "library_node_metadata": {
                        "category": "image",
                        "description": "Create an image with text rendered on it",
                    },
                    "library": "Griptape Nodes Library",
                    "node_type": "AddTextToImage",
                    "showaddparameter": False,
                    "size": {"width": 600, "height": 800},
                    "category": "image",
                },
                initial_setup=True,
            )
        ).node_name
        with GriptapeNodes.ContextManager().node(node7_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="text",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["a17453a2-0bb9-49d9-af5e-351376b226d6"],
                    initial_setup=True,
                    is_output=False,
                )
            )
    node8_name = GriptapeNodes.handle_request(
        CreateNodeGroupRequest(
            node_group_name="NodeGroup",
            metadata={
                "position": {"x": 749.0223191048804, "y": 363.6283026876037},
                "size": {"width": 1015, "height": 1062},
                "node_type": "NodeGroupNode",
                "execution_environment": {
                    "Griptape Nodes Library": {"start_flow_node": "StartFlow", "parameter_names": {}},
                    "Griptape Cloud Library": {
                        "start_flow_node": "GriptapeCloudStartFlow",
                        "parameter_names": [
                            "griptapecloudstartflow_structure_id",
                            "griptapecloudstartflow_structure_name",
                            "griptapecloudstartflow_structure_description",
                            "griptapecloudstartflow_enable_webhook_integration",
                            "griptapecloudstartflow_webhook_url",
                            "griptapecloudstartflow_integration_id",
                            "griptapecloudstartflow_payload",
                            "griptapecloudstartflow_query_params",
                            "griptapecloudstartflow_headers",
                        ],
                    },
                    "AWS Deadline Cloud Library": {
                        "start_flow_node": "DeadlineCloudStartFlow",
                        "parameter_names": [
                            "deadlinecloudstartflow_job_name",
                            "deadlinecloudstartflow_job_description",
                            "deadlinecloudstartflow_attachment_input_paths",
                            "deadlinecloudstartflow_attachment_output_paths",
                            "deadlinecloudstartflow_priority",
                            "deadlinecloudstartflow_initial_state",
                            "deadlinecloudstartflow_max_failed_tasks",
                            "deadlinecloudstartflow_max_task_retries",
                            "deadlinecloudstartflow_farm_id",
                            "deadlinecloudstartflow_queue_id",
                            "deadlinecloudstartflow_storage_profile_id",
                            "deadlinecloudstartflow_conda_channels",
                            "deadlinecloudstartflow_conda_packages",
                            "deadlinecloudstartflow_run_on_all_worker_hosts",
                            "deadlinecloudstartflow_operating_system",
                            "deadlinecloudstartflow_cpu_architecture",
                            "deadlinecloudstartflow_vcpu",
                            "deadlinecloudstartflow_memory",
                            "deadlinecloudstartflow_gpus",
                            "deadlinecloudstartflow_gpu_memory",
                            "deadlinecloudstartflow_scratch_space",
                            "deadlinecloudstartflow_add_custom_amount_requirement",
                            "deadlinecloudstartflow_add_custom_attribute_requirement",
                        ],
                    },
                },
                "subflow_name": "NodeGroup_subflow",
                "expanded_dimensions": {"width": 1015, "height": 1062},
                "left_parameters": ["exec_in", "text"],
                "right_parameters": ["exec_out", "image", "failure", "result_details"],
            },
            node_names_to_add=[node7_name],
        )
    ).node_group_name
    with GriptapeNodes.ContextManager().node(node8_name):
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="exec_in",
                tooltip="Enter control flow for exec_in.",
                type="parametercontroltype",
                input_types=["parametercontroltype"],
                output_type="parametercontroltype",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="text",
                tooltip="Enter text/string for text.",
                type="str",
                input_types=["str"],
                output_type="str",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="exec_out",
                tooltip="Enter control flow for exec_out.",
                type="parametercontroltype",
                input_types=["parametercontroltype"],
                output_type="parametercontroltype",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="image",
                tooltip="Enter ImageUrlArtifact for image.",
                type="ImageUrlArtifact",
                input_types=["ImageUrlArtifact"],
                output_type="ImageUrlArtifact",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="failure",
                tooltip="Enter control flow for failure.",
                type="parametercontroltype",
                input_types=["parametercontroltype"],
                output_type="parametercontroltype",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="result_details",
                tooltip="Enter text/string for result_details.",
                type="str",
                input_types=["str"],
                output_type="str",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True,
            )
        )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node2_name,
            source_parameter_name="exec_out",
            target_node_name=node8_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="exec_in",
            target_node_name=node7_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node2_name,
            source_parameter_name="text",
            target_node_name=node8_name,
            target_parameter_name="text",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="text",
            target_node_name=node7_name,
            target_parameter_name="text",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="exec_out",
            target_node_name=node8_name,
            target_parameter_name="exec_out",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="exec_out",
            target_node_name=node0_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="image",
            target_node_name=node8_name,
            target_parameter_name="image",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="image",
            target_node_name=node0_name,
            target_parameter_name="image",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="failure",
            target_node_name=node8_name,
            target_parameter_name="failure",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="failure",
            target_node_name=node1_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="result_details",
            target_node_name=node8_name,
            target_parameter_name="result_details",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="result_details",
            target_node_name=node1_name,
            target_parameter_name="text",
            initial_setup=True,
        )
    )
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="width",
                node_name=node0_name,
                value=top_level_unique_values_dict["4af11d7d-b32a-4d75-806f-c6a421510117"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="height",
                node_name=node0_name,
                value=top_level_unique_values_dict["4af11d7d-b32a-4d75-806f-c6a421510117"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node1_name,
                value=top_level_unique_values_dict["cf0f8055-3131-4429-b86a-d4e3410a4a4a"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node2_name,
                value=top_level_unique_values_dict["0ca3907e-1977-4f70-9cd6-6089a935ed6d"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node3_name,
                value=top_level_unique_values_dict["9f42bf68-765d-439b-802a-506111950a11"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node4_name,
                value=top_level_unique_values_dict["416d6cee-8c18-48b8-ada3-43c8655eb920"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node5_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node5_name,
                value=top_level_unique_values_dict["4f69c241-7b5d-4e05-8f6e-9011a87a4775"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node6_name,
                value=top_level_unique_values_dict["5c3b34ee-3ddc-4eeb-a49a-56bb5d44d9cf"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node8_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node8_name,
                value=top_level_unique_values_dict["b7d7f771-cf61-43ee-a858-9b56e0bf996d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node8_name,
                value=top_level_unique_values_dict["8c3a94d7-85d3-4c30-823a-93ee6638eabd"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node8_name,
                value=top_level_unique_values_dict["bd96fd97-d765-4e90-a03a-298212597afc"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node8_name,
                value=top_level_unique_values_dict["4af11d7d-b32a-4d75-806f-c6a421510117"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node8_name,
                value=top_level_unique_values_dict["4af11d7d-b32a-4d75-806f-c6a421510117"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node8_name,
                value=top_level_unique_values_dict["0ca3907e-1977-4f70-9cd6-6089a935ed6d"],
                initial_setup=True,
                is_output=False,
            )
        )
