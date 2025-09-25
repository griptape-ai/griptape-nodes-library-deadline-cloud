# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_hello_world"
# description = "A simple example demonstrating how a node can be tagged for execution on AWS Deadline Cloud within an existing workflow."
# schema_version = "0.8.0"
# engine_version_created_with = "0.56.0"
# node_libraries_referenced = [["Griptape Nodes Library", "0.50.0"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-09-25T21:54:12.527451Z
# last_modified_date = 2025-09-25T22:08:29.522359Z
#
# ///

import pickle
from griptape_nodes.node_library.library_registry import IconVariant, NodeMetadata
from griptape_nodes.retained_mode.events.connection_events import CreateConnectionRequest
from griptape_nodes.retained_mode.events.flow_events import CreateFlowRequest
from griptape_nodes.retained_mode.events.library_events import (
    GetAllInfoForAllLibrariesRequest,
    GetAllInfoForAllLibrariesResultSuccess,
    ReloadAllLibrariesRequest,
)
from griptape_nodes.retained_mode.events.node_events import CreateNodeRequest
from griptape_nodes.retained_mode.events.parameter_events import (
    AddParameterToNodeRequest,
    AlterParameterDetailsRequest,
    SetParameterValueRequest,
)
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

response = GriptapeNodes.LibraryManager().get_all_info_for_all_libraries_request(GetAllInfoForAllLibrariesRequest())

if (
    isinstance(response, GetAllInfoForAllLibrariesResultSuccess)
    and len(response.library_name_to_library_info.keys()) < 1
):
    GriptapeNodes.handle_request(ReloadAllLibrariesRequest())

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
    "7065c964-6275-456f-b1ae-2d662e5796dc": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "cf023a7c-ace7-400a-b748-1186688133d2": pickle.loads(
        b"\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rHello, world!\x94."
    ),
    "b1bdaa0a-0b6b-44f2-9059-d0a35852728f": pickle.loads(b"\x80\x04K\x00."),
    "f3a70298-c1ee-458f-a3b7-6c99211476d9": pickle.loads(
        b'\x80\x04\x95\x85\x00\x00\x00\x00\x00\x00\x00\x8c\x81This workflow demonstrates a simple "hello world" example for confirming AWS Deadline Cloud functionality is working as expected.\x94.'
    ),
    "6fe37297-06dc-488e-a911-99967a3001b6": pickle.loads(
        b'\x80\x04\x95\xd3\x01\x00\x00\x00\x00\x00\x00X\xcc\x01\x00\x00This node will be executed on Deadline Cloud. The execution_environment parameter (normally hidden) has been un-hidden and assigned to be executed on the AWS Deadline Cloud environment.\n\nThis tells Griptape Nodes to submit this node for execution.\n\nTo change a node\'s execution environment:\n1. Select the node\n2. In the Sidebar Panels, select the Properties panel\n3. Unhide the "execution_environment" Parameter\n4. Select "AWS Deadline Cloud" in the drop-down.\x94.'
    ),
    "68823bce-8791-4118-bd38-6c3f4cfce3e3": pickle.loads(
        b"\x80\x04\x95p\x00\x00\x00\x00\x00\x00\x00\x8clThis is the happy path, indicating success. Your image will appear if Deadline Cloud completes successfully.\x94."
    ),
    "3e59dc40-971e-4276-b721-281cf7e6f45a": pickle.loads(
        b"\x80\x04\x95\x84\x00\x00\x00\x00\x00\x00\x00\x8c\x80If execution in Deadline Cloud fails, this path will be executed. The Display Text will provide information about what occurred.\x94."
    ),
}

"# Create the Flow, then do work within it as context."

flow0_name = GriptapeNodes.handle_request(
    CreateFlowRequest(parent_flow_name=None, set_as_new_context=False, metadata={})
).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="AddTextToImage",
            specific_library_name="Griptape Nodes Library",
            node_name="Add Text to Image",
            metadata={
                "position": {"x": 850.6666666666667, "y": 338.6666666666667},
                "tempId": "placing-1758837148767-insxe",
                "library_node_metadata": NodeMetadata(
                    category="image",
                    description="Create an image with text rendered on it",
                    display_name="Add Text to Image",
                    tags=None,
                    icon="Type",
                    color=None,
                    group="create",
                ),
                "library": "Griptape Nodes Library",
                "node_type": "AddTextToImage",
            },
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(
            AlterParameterDetailsRequest(
                parameter_name="execution_environment",
                ui_options={"simple_dropdown": ["Local Execution", "AWS Deadline Cloud Library"], "hide": False},
                initial_setup=True,
            )
        )
    node1_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DisplayImage",
            specific_library_name="Griptape Nodes Library",
            node_name="Display Image",
            metadata={
                "position": {"x": 1456.2897033158813, "y": 353.64048865619554},
                "tempId": "placing-1758837310363-8s6gxf",
                "library_node_metadata": {"category": "image", "description": "Display an image"},
                "library": "Griptape Nodes Library",
                "node_type": "DisplayImage",
                "showaddparameter": False,
                "category": "image",
                "size": {"width": 400, "height": 296},
            },
            initial_setup=True,
        )
    ).node_name
    node2_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DisplayText",
            specific_library_name="Griptape Nodes Library",
            node_name="Display Text",
            metadata={
                "position": {"x": 1456.2897033158813, "y": 931.9650959860385},
                "tempId": "placing-1758837335086-88fhvm",
                "library_node_metadata": {"category": "text", "description": "DisplayText node"},
                "library": "Griptape Nodes Library",
                "node_type": "DisplayText",
                "showaddparameter": False,
                "category": "text",
                "size": {"width": 400, "height": 190},
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
                "position": {"x": 187.49389179755673, "y": 171.67713787085523},
                "tempId": "placing-1758837299352-bihgmj",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "category": "misc",
                "size": {"width": 400, "height": 216},
            },
            initial_setup=True,
        )
    ).node_name
    node4_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Execution Environment",
            metadata={
                "position": {"x": 765.6666666666667, "y": -181.39616055846403},
                "tempId": "placing-1758837431549-7gxmie",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "category": "misc",
                "size": {"width": 587, "height": 439},
            },
            initial_setup=True,
        )
    ).node_name
    node5_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Success Path",
            metadata={
                "position": {"x": 1456.2897033158813, "y": 146.0091278985204},
                "tempId": "placing-1758837618543-ox8yyh",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "category": "misc",
                "size": {"width": 400, "height": 182},
            },
            initial_setup=True,
        )
    ).node_name
    node6_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Unsuccessful Path",
            metadata={
                "position": {"x": 1456.2897033158813, "y": 709.9262497940123},
                "tempId": "placing-1758837618543-ox8yyh",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "category": "misc",
                "size": {"width": 401, "height": 200},
            },
            initial_setup=True,
        )
    ).node_name
    node7_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="TextInput",
            specific_library_name="Griptape Nodes Library",
            node_name="Text Input",
            metadata={
                "position": {"x": 281.36587360486317, "y": 617.1932465027377},
                "tempId": "placing-1758838088763-c9jyok",
                "library_node_metadata": NodeMetadata(
                    category="text",
                    description="TextInput node",
                    display_name="Text Input",
                    tags=None,
                    icon="text-cursor",
                    color=None,
                    group="create",
                ),
                "library": "Griptape Nodes Library",
                "node_type": "TextInput",
            },
            initial_setup=True,
        )
    ).node_name
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="exec_out",
            target_node_name=node1_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="image",
            target_node_name=node1_name,
            target_parameter_name="image",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="failure",
            target_node_name=node2_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="result_details",
            target_node_name=node2_name,
            target_parameter_name="text",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="text",
            target_node_name=node0_name,
            target_parameter_name="text",
            initial_setup=True,
        )
    )
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node0_name,
                value=top_level_unique_values_dict["7065c964-6275-456f-b1ae-2d662e5796dc"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node0_name,
                value=top_level_unique_values_dict["cf023a7c-ace7-400a-b748-1186688133d2"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="width",
                node_name=node1_name,
                value=top_level_unique_values_dict["b1bdaa0a-0b6b-44f2-9059-d0a35852728f"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="height",
                node_name=node1_name,
                value=top_level_unique_values_dict["b1bdaa0a-0b6b-44f2-9059-d0a35852728f"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node3_name,
                value=top_level_unique_values_dict["f3a70298-c1ee-458f-a3b7-6c99211476d9"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node4_name,
                value=top_level_unique_values_dict["6fe37297-06dc-488e-a911-99967a3001b6"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node5_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node5_name,
                value=top_level_unique_values_dict["68823bce-8791-4118-bd38-6c3f4cfce3e3"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node6_name,
                value=top_level_unique_values_dict["3e59dc40-971e-4276-b721-281cf7e6f45a"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node7_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node7_name,
                value=top_level_unique_values_dict["cf023a7c-ace7-400a-b748-1186688133d2"],
                initial_setup=True,
                is_output=False,
            )
        )
