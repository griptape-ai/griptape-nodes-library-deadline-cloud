# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_wedge_test"
# description = "An example demonstrating how a wedge test workflow can be triggered with parallel executions running as Jobs on AWS Deadline Cloud."
# schema_version = "0.14.0"
# engine_version_created_with = "0.64.1"
# node_libraries_referenced = [["Griptape Nodes Library", "0.52.2"], ["AWS Deadline Cloud Library", "0.65.1"]]
# node_types_used = [["AWS Deadline Cloud Library", "DeadlineCloudMultiTaskGroup"], ["Griptape Nodes Library", "Agent"], ["Griptape Nodes Library", "CreateTextList"], ["Griptape Nodes Library", "DisplayImageGrid"], ["Griptape Nodes Library", "MergeTexts"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "SeedreamImageGeneration"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-12-06T22:34:05.754692Z
# last_modified_date = 2025-12-06T22:44:38.802331Z
#
# ///

import pickle
from griptape_nodes.node_library.library_registry import IconVariant, NodeDeprecationMetadata, NodeMetadata
from griptape_nodes.retained_mode.events.connection_events import CreateConnectionRequest
from griptape_nodes.retained_mode.events.flow_events import CreateFlowRequest
from griptape_nodes.retained_mode.events.library_events import LoadLibrariesRequest
from griptape_nodes.retained_mode.events.node_events import CreateNodeRequest
from griptape_nodes.retained_mode.events.parameter_events import (
    AddParameterToNodeRequest,
    AlterParameterDetailsRequest,
    SetParameterValueRequest,
)
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

GriptapeNodes.handle_request(LoadLibrariesRequest())

context_manager = GriptapeNodes.ContextManager()

if not context_manager.has_current_workflow():
    context_manager.push_workflow(workflow_name="deadline_cloud_wedge_test")

"""
1. We've collated all of the unique parameter values into a dictionary so that we do not have to duplicate them.
   This minimizes the size of the code, especially for large objects like serialized image files.
2. We're using a prefix so that it's clear which Flow these values are associated with.
3. The values are serialized using pickle, which is a binary format. This makes them harder to read, but makes
   them consistently save and load. It allows us to serialize complex objects like custom classes, which otherwise
   would be difficult to serialize.
"""
top_level_unique_values_dict = {
    "f87735ae-2a17-4f20-a509-8e45bdf37463": pickle.loads(
        b"\x80\x04\x95\xb6\x01\x00\x00\x00\x00\x00\x00X\xaf\x01\x00\x00# Overview\n\nExecuting this workflow will result in the below Deadline Cloud Multi Task Group being published to AWS Deadline Cloud, and submitting 1 job with 3 parallel tasks to generate images for all 3 of the input subjects.\n\nThe Deadline Cloud Multi Task Group is an implementation of a Subflow Node Group. It is used to iterate over the input list, creating a task to run the Group body for each input, and collect the results.\x94."
    ),
    "ca182d5a-a447-4fd5-8042-eb1134b00743": pickle.loads(
        b"\x80\x04\x95!\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x08Capybara\x94\x8c\x07Giraffe\x94\x8c\x04Lion\x94e."
    ),
    "4e341549-e43c-4093-9483-b55534eecaae": pickle.loads(
        b"\x80\x04\x95\x0c\x00\x00\x00\x00\x00\x00\x00\x8c\x08Capybara\x94."
    ),
    "b951e35d-872e-47b0-9846-2473e4f7cf1a": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07Giraffe\x94."
    ),
    "9c7009e7-5979-4048-bf45-81aed6fb27eb": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04Lion\x94."
    ),
    "fc61dea4-0ade-4b84-9068-2d0f24f646d7": pickle.loads(
        b"\x80\x04\x95!\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x08Capybara\x94\x8c\x07Giraffe\x94\x8c\x04Lion\x94e."
    ),
    "923a9956-4213-4b2e-b088-503450433947": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04grid\x94."
    ),
    "72de1831-72ea-47ff-9468-64325be8698b": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04left\x94."
    ),
    "2e5a0dbd-1215-48c6-927d-d2030c0cda41": pickle.loads(b"\x80\x04K\x03."),
    "e7d7984c-cf3b-45a8-b152-0813b7e73502": pickle.loads(b"\x80\x04K\n."),
    "020ff7ba-e981-42ed-b76b-f3a9189df5ef": pickle.loads(b"\x80\x04K\x08."),
    "d37e610a-76df-4364-af0d-23d8eee3af58": pickle.loads(b"\x80\x04\x88."),
    "62f9e599-15af-4b42-9691-0cf17a76e92c": pickle.loads(b"\x80\x04\x89."),
    "f1d8b187-efc0-4852-b0d5-7f7310843733": pickle.loads(
        b"\x80\x04\x95\r\x00\x00\x00\x00\x00\x00\x00\x8c\t#000000ff\x94."
    ),
    "59a229c1-89ca-4d53-bd1f-9283586c20c1": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06custom\x94."
    ),
    "55c6950f-2c21-43eb-b271-1237ee1bfcf3": pickle.loads(
        b"\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00\x8c\x111080p (1920x1080)\x94."
    ),
    "c31ea910-75a2-47b6-a0a4-9b9fb6ef0705": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\xb0\x04."),
    "c0ddbbe4-8bc9-433d-aa08-7e99b0186730": pickle.loads(
        b"\x80\x04\x95\x07\x00\x00\x00\x00\x00\x00\x00\x8c\x03png\x94."
    ),
    "697c2137-49be-479b-901d-eb156d54eff6": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "d5e480de-a2a2-4861-9f4c-6e7cce3f8409": pickle.loads(
        b"\x80\x04\x95\x0e\x00\x00\x00\x00\x00\x00\x00\x8c\nWedge Test\x94."
    ),
    "3bd3791c-3138-467f-a13c-e9935110acba": pickle.loads(
        b"\x80\x04\x95$\x00\x00\x00\x00\x00\x00\x00\x8c Multi task Job on Deadline Cloud\x94."
    ),
    "64e63b24-8182-46a6-9e69-b119cb41ca1d": pickle.loads(b"\x80\x04]\x94."),
    "bc6316bf-b4bf-4677-bcad-23947e90ce2a": pickle.loads(b"\x80\x04]\x94."),
    "6924492b-1328-498a-86d6-d4fcaf7c7538": pickle.loads(b"\x80\x04K2."),
    "473dd81a-0bca-4694-8fd4-8d73593c55e1": pickle.loads(
        b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05READY\x94."
    ),
    "f0ae232b-03b1-425b-b8fa-975acbe4cc39": pickle.loads(b"\x80\x04K\x00."),
    "2278c50e-1852-48c8-b56b-844134059181": pickle.loads(
        b"\x80\x04\x95)\x00\x00\x00\x00\x00\x00\x00\x8c%farm-7bbde5411d444d039f12b30e007658fd\x94."
    ),
    "d3b0b7a7-337c-4a7e-b27f-a521e73d9d9d": pickle.loads(
        b"\x80\x04\x95*\x00\x00\x00\x00\x00\x00\x00\x8c&queue-1c93aa55070f44279d03ed7a13918099\x94."
    ),
    "089bd74b-52e8-480c-b2ee-b47ec277de3a": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "08e01a71-74ad-471d-ab47-5e3531e0c36f": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bconda-forge\x94."
    ),
    "b7ddd111-7076-414a-8726-7296084a5334": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bpython=3.12\x94."
    ),
    "eed45383-89c5-40a6-9b8b-2d3732522ebc": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06gpt-4o\x94."
    ),
    "ea0900e8-389f-40eb-945d-d558c96655ae": pickle.loads(
        b"\x80\x04\x954\x00\x00\x00\x00\x00\x00\x00\x8c0Create a detailed image generation prompt for a:\x94."
    ),
    "a5748387-6ea2-412b-bd73-f7477fc14fdd": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "37285d0e-de56-4d33-9a2a-a64be94ac368": pickle.loads(b"\x80\x04]\x94."),
    "d981c1d9-f49f-4753-9f64-1efbbe3e1481": pickle.loads(b"\x80\x04]\x94."),
    "706a547d-6bee-436a-a44f-f128433e8eaf": pickle.loads(b"\x80\x04\x89."),
    "4af9344c-45cd-4a14-974b-f06b9d853e57": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04\\n\\n\x94."
    ),
    "3f18a94a-ace6-4941-834b-58c06396c0f7": pickle.loads(
        b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x0cseedream-4.5\x94."
    ),
    "6f151601-41b7-41ae-b8a9-e4544ef6ea94": pickle.loads(b"\x80\x04]\x94."),
    "f341637a-9399-4c2b-8592-47b56f371f49": pickle.loads(
        b"\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00\x8c\x022K\x94."
    ),
    "fcd68c36-3829-4e19-834c-95482b860283": pickle.loads(
        b"\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00J\xff\xff\xff\xff."
    ),
    "e6aeee4c-8df8-4893-8e57-bc53e5673cdd": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00G@\x04\x00\x00\x00\x00\x00\x00."
    ),
}

"# Create the Flow, then do work within it as context."

flow0_name = GriptapeNodes.handle_request(
    CreateFlowRequest(parent_flow_name=None, flow_name="ControlFlow_1", set_as_new_context=False, metadata={})
).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Note",
            metadata={
                "position": {"x": 10.220001250459006, "y": 72.93411539432404},
                "tempId": "placing-1765060114455-9hlvj",
                "library_node_metadata": NodeMetadata(
                    category="misc",
                    description="Create a note node to provide helpful context in your workflow",
                    display_name="Note",
                    tags=None,
                    icon="notepad-text",
                    color=None,
                    group="create",
                    deprecation=None,
                    is_node_group=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "size": {"width": 2194, "height": 274},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    node1_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="CreateTextList",
            specific_library_name="Griptape Nodes Library",
            node_name="Create Text List",
            metadata={
                "position": {"x": -972.498247610275, "y": 375.9590046278638},
                "tempId": "placing-1765060150191-cv09t8",
                "library_node_metadata": NodeMetadata(
                    category="lists",
                    description="Creates a list of text items",
                    display_name="Create Text List",
                    tags=None,
                    icon=None,
                    color=None,
                    group="create",
                    deprecation=None,
                    is_node_group=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "CreateTextList",
                "showaddparameter": False,
                "size": {"width": 669, "height": 1050},
                "category": "lists",
            },
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="items_ParameterListUniqueParamID_f21334b88f9248b5928497c8de05e92c",
                tooltip="List of text items to add to",
                type="str",
                input_types=["str"],
                output_type="str",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=False,
                is_user_defined=True,
                settable=True,
                parent_container_name="items",
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="items_ParameterListUniqueParamID_3ca5b9e3ba9a40bc879ee4df68c7929d",
                tooltip="List of text items to add to",
                type="str",
                input_types=["str"],
                output_type="str",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=False,
                is_user_defined=True,
                settable=True,
                parent_container_name="items",
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="items_ParameterListUniqueParamID_e525d5d0e55240498d370869f6cd03df",
                tooltip="List of text items to add to",
                type="str",
                input_types=["str"],
                output_type="str",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=False,
                is_user_defined=True,
                settable=True,
                parent_container_name="items",
                initial_setup=True,
            )
        )
    node2_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DisplayImageGrid",
            specific_library_name="Griptape Nodes Library",
            node_name="Display Image Grid",
            metadata={
                "position": {"x": 2618.934665051889, "y": 437.32043825563596},
                "tempId": "placing-1765060366449-u6cfvj",
                "library_node_metadata": NodeMetadata(
                    category="image",
                    description="Display multiple images in a grid or masonry layout with customizable styling options",
                    display_name="Display Image Grid",
                    tags=None,
                    icon="grid-3x3",
                    color=None,
                    group="display",
                    deprecation=None,
                    is_node_group=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "DisplayImageGrid",
                "showaddparameter": False,
                "size": {"width": 1354, "height": 1054},
                "category": "image",
            },
            initial_setup=True,
        )
    ).node_name
    """# Create the Flow, then do work within it as context."""
    flow1_name = GriptapeNodes.handle_request(
        CreateFlowRequest(
            parent_flow_name=flow0_name,
            flow_name="Deadline Cloud Multi Task Group_subflow",
            set_as_new_context=False,
            metadata={"flow_type": "NodeGroupFlow"},
        )
    ).flow_name
    with GriptapeNodes.ContextManager().flow(flow1_name):
        node3_name = GriptapeNodes.handle_request(
            CreateNodeRequest(
                node_type="Agent",
                specific_library_name="Griptape Nodes Library",
                node_name="Agent",
                metadata={
                    "position": {"x": 927.3535877315443, "y": 98.5},
                    "tempId": "placing-1765060202129-7rehv",
                    "library_node_metadata": NodeMetadata(
                        category="agents",
                        description="Creates an AI agent with conversation memory and the ability to use tools",
                        display_name="Agent",
                        tags=None,
                        icon=None,
                        color=None,
                        group="create",
                        deprecation=None,
                        is_node_group=None,
                    ),
                    "library": "Griptape Nodes Library",
                    "node_type": "Agent",
                    "showaddparameter": False,
                    "size": {"width": 600, "height": 864},
                    "category": "agents",
                },
                initial_setup=True,
            )
        ).node_name
        node4_name = GriptapeNodes.handle_request(
            CreateNodeRequest(
                node_type="MergeTexts",
                specific_library_name="Griptape Nodes Library",
                node_name="Merge Texts",
                metadata={
                    "position": {"x": 196.40033061799159, "y": 98.5},
                    "tempId": "placing-1765060214987-mg88db",
                    "library_node_metadata": NodeMetadata(
                        category="text",
                        description="MergeTexts node",
                        display_name="Merge Texts",
                        tags=None,
                        icon="merge",
                        color=None,
                        group="merge",
                        deprecation=None,
                        is_node_group=None,
                    ),
                    "library": "Griptape Nodes Library",
                    "node_type": "MergeTexts",
                    "showaddparameter": False,
                    "size": {"width": 610, "height": 841},
                    "category": "text",
                },
                initial_setup=True,
            )
        ).node_name
        node5_name = GriptapeNodes.handle_request(
            CreateNodeRequest(
                node_type="SeedreamImageGeneration",
                specific_library_name="Griptape Nodes Library",
                node_name="Seedream Image Generation",
                metadata={
                    "position": {"x": 1642.2876360903058, "y": 98.5},
                    "tempId": "placing-1765060255639-ada8z",
                    "library_node_metadata": {
                        "category": "image",
                        "description": "Generate images using Seedream models (seedream-4.0, seedream-3.0-t2i) via Griptape model proxy",
                    },
                    "library": "Griptape Nodes Library",
                    "node_type": "SeedreamImageGeneration",
                    "showaddparameter": False,
                    "size": {"width": 611, "height": 865},
                    "category": "image",
                },
                initial_setup=True,
            )
        ).node_name
        GriptapeNodes.handle_request(
            CreateConnectionRequest(
                source_node_name=node4_name,
                source_parameter_name="output",
                target_node_name=node3_name,
                target_parameter_name="prompt",
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            CreateConnectionRequest(
                source_node_name=node3_name,
                source_parameter_name="output",
                target_node_name=node5_name,
                target_parameter_name="prompt",
                initial_setup=True,
            )
        )
        with GriptapeNodes.ContextManager().node(node3_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="model",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["eed45383-89c5-40a6-9b8b-2d3732522ebc"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="prompt",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["ea0900e8-389f-40eb-945d-d558c96655ae"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="additional_context",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["a5748387-6ea2-412b-bd73-f7477fc14fdd"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="tools",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["37285d0e-de56-4d33-9a2a-a64be94ac368"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="rulesets",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["d981c1d9-f49f-4753-9f64-1efbbe3e1481"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["a5748387-6ea2-412b-bd73-f7477fc14fdd"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="include_details",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["706a547d-6bee-436a-a44f-f128433e8eaf"],
                    initial_setup=True,
                    is_output=False,
                )
            )
        with GriptapeNodes.ContextManager().node(node4_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="input_1",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["ea0900e8-389f-40eb-945d-d558c96655ae"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="input_2",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["a5748387-6ea2-412b-bd73-f7477fc14fdd"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="merge_string",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["4af9344c-45cd-4a14-974b-f06b9d853e57"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="whitespace",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["706a547d-6bee-436a-a44f-f128433e8eaf"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["ea0900e8-389f-40eb-945d-d558c96655ae"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["ea0900e8-389f-40eb-945d-d558c96655ae"],
                    initial_setup=True,
                    is_output=True,
                )
            )
        with GriptapeNodes.ContextManager().node(node5_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="model",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["3f18a94a-ace6-4941-834b-58c06396c0f7"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="images",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["6f151601-41b7-41ae-b8a9-e4544ef6ea94"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="size",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["f341637a-9399-4c2b-8592-47b56f371f49"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="seed",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["fcd68c36-3829-4e19-834c-95482b860283"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="guidance_scale",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["e6aeee4c-8df8-4893-8e57-bc53e5673cdd"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["706a547d-6bee-436a-a44f-f128433e8eaf"],
                    initial_setup=True,
                    is_output=False,
                )
            )
    node6_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DeadlineCloudMultiTaskGroup",
            specific_library_name="AWS Deadline Cloud Library",
            node_name="Deadline Cloud Multi Task Group",
            metadata={
                "position": {"x": -138.7034571549159, "y": 421.9590046278638},
                "size": {"width": 2530, "height": 1054},
                "library_node_metadata": NodeMetadata(
                    category="aws_deadline_cloud/execution",
                    description="SubflowNodeGroup that iterates over a list of input to run a subflow as a Task per input, submitted as a single Job.",
                    display_name="Deadline Cloud Multi Task Group",
                    tags=None,
                    icon=None,
                    color=None,
                    group=None,
                    deprecation=None,
                    is_node_group=True,
                ),
                "library": "AWS Deadline Cloud Library",
                "node_type": "DeadlineCloudMultiTaskGroup",
                "is_node_group": True,
                "color": "#00c951",
                "hideaddparameter": True,
                "execution_environment": {
                    "Griptape Nodes Library": {"start_flow_node": "StartFlow", "parameter_names": {}},
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
                "left_parameters": ["items", "current_item"],
                "right_parameters": ["new_item_to_add", "results"],
                "subflow_name": "Deadline Cloud Multi Task Group_subflow",
                "expanded_dimensions": {"width": 2530, "height": 1054},
            },
            node_names_to_add=[node3_name, node4_name, node5_name],
        )
    ).node_name
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node1_name,
            source_parameter_name="output",
            target_node_name=node6_name,
            target_parameter_name="items",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node6_name,
            source_parameter_name="current_item",
            target_node_name=node4_name,
            target_parameter_name="input_2",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="image_url",
            target_node_name=node6_name,
            target_parameter_name="new_item_to_add",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node6_name,
            source_parameter_name="results",
            target_node_name=node2_name,
            target_parameter_name="images",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node4_name,
            source_parameter_name="output",
            target_node_name=node3_name,
            target_parameter_name="prompt",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node3_name,
            source_parameter_name="output",
            target_node_name=node5_name,
            target_parameter_name="prompt",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node4_name,
            source_parameter_name="output",
            target_node_name=node3_name,
            target_parameter_name="prompt",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node3_name,
            source_parameter_name="output",
            target_node_name=node5_name,
            target_parameter_name="prompt",
            initial_setup=True,
        )
    )
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node0_name,
                value=top_level_unique_values_dict["f87735ae-2a17-4f20-a509-8e45bdf37463"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items",
                node_name=node1_name,
                value=top_level_unique_values_dict["ca182d5a-a447-4fd5-8042-eb1134b00743"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_f21334b88f9248b5928497c8de05e92c",
                node_name=node1_name,
                value=top_level_unique_values_dict["4e341549-e43c-4093-9483-b55534eecaae"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_3ca5b9e3ba9a40bc879ee4df68c7929d",
                node_name=node1_name,
                value=top_level_unique_values_dict["b951e35d-872e-47b0-9846-2473e4f7cf1a"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_e525d5d0e55240498d370869f6cd03df",
                node_name=node1_name,
                value=top_level_unique_values_dict["9c7009e7-5979-4048-bf45-81aed6fb27eb"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node1_name,
                value=top_level_unique_values_dict["fc61dea4-0ade-4b84-9068-2d0f24f646d7"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node1_name,
                value=top_level_unique_values_dict["fc61dea4-0ade-4b84-9068-2d0f24f646d7"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="layout_style",
                node_name=node2_name,
                value=top_level_unique_values_dict["923a9956-4213-4b2e-b088-503450433947"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="grid_justification",
                node_name=node2_name,
                value=top_level_unique_values_dict["72de1831-72ea-47ff-9468-64325be8698b"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="columns",
                node_name=node2_name,
                value=top_level_unique_values_dict["2e5a0dbd-1215-48c6-927d-d2030c0cda41"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="spacing",
                node_name=node2_name,
                value=top_level_unique_values_dict["e7d7984c-cf3b-45a8-b152-0813b7e73502"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="border_radius",
                node_name=node2_name,
                value=top_level_unique_values_dict["020ff7ba-e981-42ed-b76b-f3a9189df5ef"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="crop_to_fit",
                node_name=node2_name,
                value=top_level_unique_values_dict["d37e610a-76df-4364-af0d-23d8eee3af58"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="transparent_bg",
                node_name=node2_name,
                value=top_level_unique_values_dict["62f9e599-15af-4b42-9691-0cf17a76e92c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="background_color",
                node_name=node2_name,
                value=top_level_unique_values_dict["f1d8b187-efc0-4852-b0d5-7f7310843733"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_image_size",
                node_name=node2_name,
                value=top_level_unique_values_dict["59a229c1-89ca-4d53-bd1f-9283586c20c1"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_preset",
                node_name=node2_name,
                value=top_level_unique_values_dict["55c6950f-2c21-43eb-b271-1237ee1bfcf3"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_image_width",
                node_name=node2_name,
                value=top_level_unique_values_dict["c31ea910-75a2-47b6-a0a4-9b9fb6ef0705"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_format",
                node_name=node2_name,
                value=top_level_unique_values_dict["c0ddbbe4-8bc9-433d-aa08-7e99b0186730"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node6_name,
                value=top_level_unique_values_dict["697c2137-49be-479b-901d-eb156d54eff6"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node6_name,
                value=top_level_unique_values_dict["d5e480de-a2a2-4861-9f4c-6e7cce3f8409"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node6_name,
                value=top_level_unique_values_dict["3bd3791c-3138-467f-a13c-e9935110acba"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_input_paths",
                node_name=node6_name,
                value=top_level_unique_values_dict["64e63b24-8182-46a6-9e69-b119cb41ca1d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_output_paths",
                node_name=node6_name,
                value=top_level_unique_values_dict["bc6316bf-b4bf-4677-bcad-23947e90ce2a"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_priority",
                node_name=node6_name,
                value=top_level_unique_values_dict["6924492b-1328-498a-86d6-d4fcaf7c7538"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_initial_state",
                node_name=node6_name,
                value=top_level_unique_values_dict["473dd81a-0bca-4694-8fd4-8d73593c55e1"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node6_name,
                value=top_level_unique_values_dict["f0ae232b-03b1-425b-b8fa-975acbe4cc39"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node6_name,
                value=top_level_unique_values_dict["f0ae232b-03b1-425b-b8fa-975acbe4cc39"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_farm_id",
                node_name=node6_name,
                value=top_level_unique_values_dict["2278c50e-1852-48c8-b56b-844134059181"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_queue_id",
                node_name=node6_name,
                value=top_level_unique_values_dict["d3b0b7a7-337c-4a7e-b27f-a521e73d9d9d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_storage_profile_id",
                node_name=node6_name,
                value=top_level_unique_values_dict["089bd74b-52e8-480c-b2ee-b47ec277de3a"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_channels",
                node_name=node6_name,
                value=top_level_unique_values_dict["08e01a71-74ad-471d-ab47-5e3531e0c36f"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_packages",
                node_name=node6_name,
                value=top_level_unique_values_dict["b7ddd111-7076-414a-8726-7296084a5334"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_run_on_all_worker_hosts",
                node_name=node6_name,
                value=top_level_unique_values_dict["d37e610a-76df-4364-af0d-23d8eee3af58"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items",
                node_name=node6_name,
                value=top_level_unique_values_dict["fc61dea4-0ade-4b84-9068-2d0f24f646d7"],
                initial_setup=True,
                is_output=False,
            )
        )
