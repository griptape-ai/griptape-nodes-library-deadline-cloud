# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_hello_world"
# description = "A simple example demonstrating how a node can be tagged for execution on AWS Deadline Cloud within an existing workflow."
# schema_version = "0.11.0"
# engine_version_created_with = "0.59.3"
# node_libraries_referenced = [["Griptape Nodes Library", "0.50.0"]]
# node_types_used = [["Griptape Nodes Library", "AddTextToImage"], ["Griptape Nodes Library", "DisplayImage"], ["Griptape Nodes Library", "DisplayText"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "TextInput"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-10-22T05:04:16.751722Z
# last_modified_date = 2025-10-22T05:04:16.769039Z
#
# ///

import pickle
from griptape_nodes.node_library.library_registry import IconVariant, NodeDeprecationMetadata, NodeMetadata
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

response = GriptapeNodes.handle_request(GetAllInfoForAllLibrariesRequest())

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
    "afcbc8ea-4fca-486f-ae0d-7c3b047c57a0": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "4e9d3459-c598-4cba-a12f-239d2a9dc067": pickle.loads(
        b"\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rHello, world!\x94."
    ),
    "d1bc7681-9352-4839-9797-b1d03d723a4b": pickle.loads(b"\x80\x04K\x00."),
    "d283d5c6-ff0d-4a2e-8046-dd3040256a52": pickle.loads(
        b'\x80\x04\x95\x85\x00\x00\x00\x00\x00\x00\x00\x8c\x81This workflow demonstrates a simple "hello world" example for confirming AWS Deadline Cloud functionality is working as expected.\x94.'
    ),
    "3121dc10-8b5e-4fb3-92f8-4c8beb678743": pickle.loads(
        b'\x80\x04\x95\xd3\x01\x00\x00\x00\x00\x00\x00X\xcc\x01\x00\x00This node will be executed on Deadline Cloud. The execution_environment parameter (normally hidden) has been un-hidden and assigned to be executed on the AWS Deadline Cloud environment.\n\nThis tells Griptape Nodes to submit this node for execution.\n\nTo change a node\'s execution environment:\n1. Select the node\n2. In the Sidebar Panels, select the Properties panel\n3. Unhide the "execution_environment" Parameter\n4. Select "AWS Deadline Cloud" in the drop-down.\x94.'
    ),
    "64f43dc6-4563-490f-a6ee-9b8eea182b97": pickle.loads(
        b"\x80\x04\x95p\x00\x00\x00\x00\x00\x00\x00\x8clThis is the happy path, indicating success. Your image will appear if Deadline Cloud completes successfully.\x94."
    ),
    "6f1ade01-3401-4832-b5f7-156799139db3": pickle.loads(
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
                    deprecation=None,
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
                ui_options={
                    "simple_dropdown": ["Local Execution", "AWS Deadline Cloud Library"],
                    "show_search": True,
                    "search_filter": "",
                    "hide": False,
                },
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
                "library_node_metadata": NodeMetadata(
                    category="image",
                    description="Display an image",
                    display_name="Display Image",
                    tags=None,
                    icon=None,
                    color=None,
                    group="display",
                    deprecation=None,
                ),
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
                "library_node_metadata": NodeMetadata(
                    category="misc",
                    description="Create a note node to provide helpful context in your workflow",
                    display_name="Note",
                    tags=None,
                    icon="notepad-text",
                    color=None,
                    group="create",
                    deprecation=None,
                ),
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
                "library_node_metadata": NodeMetadata(
                    category="misc",
                    description="Create a note node to provide helpful context in your workflow",
                    display_name="Note",
                    tags=None,
                    icon="notepad-text",
                    color=None,
                    group="create",
                    deprecation=None,
                ),
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
                "library_node_metadata": NodeMetadata(
                    category="misc",
                    description="Create a note node to provide helpful context in your workflow",
                    display_name="Note",
                    tags=None,
                    icon="notepad-text",
                    color=None,
                    group="create",
                    deprecation=None,
                ),
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
                "library_node_metadata": NodeMetadata(
                    category="misc",
                    description="Create a note node to provide helpful context in your workflow",
                    display_name="Note",
                    tags=None,
                    icon="notepad-text",
                    color=None,
                    group="create",
                    deprecation=None,
                ),
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
                    deprecation=None,
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
                value=top_level_unique_values_dict["afcbc8ea-4fca-486f-ae0d-7c3b047c57a0"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node0_name,
                value=top_level_unique_values_dict["4e9d3459-c598-4cba-a12f-239d2a9dc067"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="width",
                node_name=node1_name,
                value=top_level_unique_values_dict["d1bc7681-9352-4839-9797-b1d03d723a4b"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="height",
                node_name=node1_name,
                value=top_level_unique_values_dict["d1bc7681-9352-4839-9797-b1d03d723a4b"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node3_name,
                value=top_level_unique_values_dict["d283d5c6-ff0d-4a2e-8046-dd3040256a52"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node4_name,
                value=top_level_unique_values_dict["3121dc10-8b5e-4fb3-92f8-4c8beb678743"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node5_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node5_name,
                value=top_level_unique_values_dict["64f43dc6-4563-490f-a6ee-9b8eea182b97"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node6_name,
                value=top_level_unique_values_dict["6f1ade01-3401-4832-b5f7-156799139db3"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node7_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node7_name,
                value=top_level_unique_values_dict["4e9d3459-c598-4cba-a12f-239d2a9dc067"],
                initial_setup=True,
                is_output=False,
            )
        )
