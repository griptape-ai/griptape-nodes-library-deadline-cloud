# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_wedge_test"
# schema_version = "0.14.0"
# engine_version_created_with = "0.66.2"
# node_libraries_referenced = [["Griptape Nodes Library", "0.55.0"], ["AWS Deadline Cloud Library", "0.66.3"]]
# node_types_used = [["AWS Deadline Cloud Library", "DeadlineCloudMultiTaskGroup"], ["Griptape Nodes Library", "Agent"], ["Griptape Nodes Library", "CreateTextList"], ["Griptape Nodes Library", "DisplayImageGrid"], ["Griptape Nodes Library", "MergeTexts"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "SeedreamImageGeneration"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-12-31T19:36:08.410350Z
# last_modified_date = 2025-12-31T19:36:08.659191Z
#
# ///

import pickle
from griptape.artifacts.image_url_artifact import ImageUrlArtifact
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
    "191c2c93-16af-4775-8d24-3ba10465028b": pickle.loads(
        b"\x80\x04\x95\xe7\x01\x00\x00\x00\x00\x00\x00X\xe0\x01\x00\x00# Overview\n\nExecuting this workflow will result in the below Deadline Cloud Multi Task Group being published to AWS Deadline Cloud, and submitting 1 job with 3 parallel tasks to generate images for all 3 of the input subjects.\n\nThe Deadline Cloud Multi Task Group is an implementation of a Subflow Node Group. It is used to iterate over the input list, creating a task to run the Group body for each input, and collect the results.\n\nClick 'Run Workflow' to kick off the execution.\x94."
    ),
    "01f74ed5-692f-4b67-8088-a00d09a1c9c1": pickle.loads(
        b"\x80\x04\x95!\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x08Capybara\x94\x8c\x07Giraffe\x94\x8c\x04Lion\x94e."
    ),
    "c4511fea-ce0e-4134-958a-e42fc7437beb": pickle.loads(
        b"\x80\x04\x95\x0c\x00\x00\x00\x00\x00\x00\x00\x8c\x08Capybara\x94."
    ),
    "754a09d5-7e1a-4316-b6e9-abdbec93a19d": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07Giraffe\x94."
    ),
    "c484f041-778d-4a14-ac2e-43ffdf97441c": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04Lion\x94."
    ),
    "ccdc067e-fe0c-4256-9e98-d56282ebd512": pickle.loads(
        b"\x80\x04\x95!\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x08Capybara\x94\x8c\x07Giraffe\x94\x8c\x04Lion\x94e."
    ),
    "1a7c93fb-6c9b-45fe-a297-388c4b9762ec": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04grid\x94."
    ),
    "7f11c6e4-e28f-4a11-a7bb-8c2fb225fecf": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04left\x94."
    ),
    "c85e10f2-2b29-40b5-9048-e244b3bb3f14": pickle.loads(b"\x80\x04K\x03."),
    "46367adf-a58a-4aa9-a000-37e7df536672": pickle.loads(b"\x80\x04K\n."),
    "4aba6118-4a31-4826-a73b-f44005594bc7": pickle.loads(b"\x80\x04K\x08."),
    "6cdeb7d5-004a-44d0-af72-add3c028df0f": pickle.loads(b"\x80\x04\x88."),
    "c4c4ae90-8152-491e-ab29-b71de163b4d5": pickle.loads(b"\x80\x04\x89."),
    "106aded4-a2c9-4a87-9d26-f1369305bdd5": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07#000000\x94."
    ),
    "ef984dcd-d810-40f3-a8f9-1ea22e784962": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06custom\x94."
    ),
    "b1310837-09a7-4258-814b-31ac2d957a38": pickle.loads(
        b"\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00\x8c\x111080p (1920x1080)\x94."
    ),
    "8bd0a338-b7b2-414c-bfbd-53c3ccd88d33": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\xb0\x04."),
    "7ab23d00-696f-49ac-a33a-8942e989ede8": pickle.loads(
        b"\x80\x04\x95\x07\x00\x00\x00\x00\x00\x00\x00\x8c\x03png\x94."
    ),
    "51285cec-f932-4d1c-ad5c-ef2556659495": pickle.loads(
        b"\x80\x04\x95\xc3\x01\x00\x00\x00\x00\x00\x00\x8c%griptape.artifacts.image_url_artifact\x94\x8c\x10ImageUrlArtifact\x94\x93\x94)\x81\x94}\x94(\x8c\x04type\x94h\x01\x8c\x0bmodule_name\x94h\x00\x8c\x02id\x94\x8c fce65e450d8344ca997b15a9fe44f1b0\x94\x8c\treference\x94N\x8c\x04meta\x94}\x94\x8c\x04name\x94h\x08\x8c\x16encoding_error_handler\x94\x8c\x06strict\x94\x8c\x08encoding\x94\x8c\x05utf-8\x94\x8c\x05value\x94\x8c\xddhttp://localhost:8124/workspace/libraries/griptape-nodes-library-deadline-cloud/griptape_nodes_library_deadline_cloud/workflows/templates/staticfiles/deadline_cloud_wedge_test_DisplayImageGrid_placeholder.png?t=1767209702\x94ub."
    ),
    "89f439c0-9eaa-4895-8d71-c8ddf196f31e": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "52a0e100-c349-47b4-a7a1-d7a4c2200372": pickle.loads(
        b"\x80\x04\x95\x0e\x00\x00\x00\x00\x00\x00\x00\x8c\nWedge Test\x94."
    ),
    "5e77136a-d81e-4725-a665-9494effd2b87": pickle.loads(
        b"\x80\x04\x95$\x00\x00\x00\x00\x00\x00\x00\x8c Multi task Job on Deadline Cloud\x94."
    ),
    "3bda9f4e-c485-442f-b14d-f21d306ac2f5": pickle.loads(b"\x80\x04]\x94."),
    "e99a54da-23ab-4c95-9da5-772b578fee3a": pickle.loads(b"\x80\x04]\x94."),
    "58c7f348-9d4a-43b6-bbf8-d7b0b7d698b2": pickle.loads(b"\x80\x04K2."),
    "54dba5b3-700f-42bf-9b14-6c45e5a99d04": pickle.loads(
        b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05READY\x94."
    ),
    "a3c27e7b-6c10-49c8-bcc7-c0a92479bda2": pickle.loads(b"\x80\x04K\x00."),
    "fb67b4ed-a502-4b29-8081-cbff0537b0e2": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bconda-forge\x94."
    ),
    "59a94ea3-185d-4185-9bb6-79482a1d900f": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bpython=3.12\x94."
    ),
    "2c5bcbf6-e216-409e-b365-67973843b498": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06gpt-4o\x94."
    ),
    "7ad17f66-eec7-47e1-a367-131ccc0aabe9": pickle.loads(
        b"\x80\x04\x954\x00\x00\x00\x00\x00\x00\x00\x8c0Create a detailed image generation prompt for a:\x94."
    ),
    "70436721-40f7-4b3c-a882-a703fad5f70b": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "fe3137b5-742b-4fd3-b5f8-aaf1d1f9793c": pickle.loads(b"\x80\x04]\x94."),
    "2e974a55-2bdd-4756-925f-3ab600ab188d": pickle.loads(b"\x80\x04]\x94."),
    "f0f4b64d-3a1d-431a-9835-0a905bf437c4": pickle.loads(b"\x80\x04\x89."),
    "e2e8c898-65ae-4665-b454-e9b854665982": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04\\n\\n\x94."
    ),
    "0215b164-6a8d-443b-a066-e5bd7cfa86da": pickle.loads(
        b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x0cseedream-4.5\x94."
    ),
    "2bd3049f-84fe-4a9a-810b-7803f22275f7": pickle.loads(b"\x80\x04]\x94."),
    "ce0d0075-832d-420e-8525-d7c4fc193e8a": pickle.loads(
        b"\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00\x8c\x022K\x94."
    ),
    "91bd1e20-dfcd-44c4-a82a-8fae1ba78a93": pickle.loads(
        b"\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00J\xff\xff\xff\xff."
    ),
    "dbe9a2ba-3a67-46c9-8e4e-eefe39a9f59e": pickle.loads(b"\x80\x04K\n."),
    "0e3eb9b7-3130-4abe-8521-0c1f25cefe12": pickle.loads(
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
                    "library_node_metadata": NodeMetadata(
                        category="image",
                        description="Generate images using Seedream models (seedream-4.0, seedream-3.0-t2i) via Griptape model proxy",
                        display_name="Seedream Image Generation",
                        tags=None,
                        icon="Sparkles",
                        color=None,
                        group="create",
                        deprecation=None,
                        is_node_group=None,
                    ),
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
                    value=top_level_unique_values_dict["2c5bcbf6-e216-409e-b365-67973843b498"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="prompt",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["7ad17f66-eec7-47e1-a367-131ccc0aabe9"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="additional_context",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["70436721-40f7-4b3c-a882-a703fad5f70b"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="tools",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["fe3137b5-742b-4fd3-b5f8-aaf1d1f9793c"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="rulesets",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["2e974a55-2bdd-4756-925f-3ab600ab188d"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["70436721-40f7-4b3c-a882-a703fad5f70b"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="include_details",
                    node_name=node3_name,
                    value=top_level_unique_values_dict["f0f4b64d-3a1d-431a-9835-0a905bf437c4"],
                    initial_setup=True,
                    is_output=False,
                )
            )
        with GriptapeNodes.ContextManager().node(node4_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="input_1",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["7ad17f66-eec7-47e1-a367-131ccc0aabe9"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="input_2",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["70436721-40f7-4b3c-a882-a703fad5f70b"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="merge_string",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["e2e8c898-65ae-4665-b454-e9b854665982"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="whitespace",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["f0f4b64d-3a1d-431a-9835-0a905bf437c4"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["7ad17f66-eec7-47e1-a367-131ccc0aabe9"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output",
                    node_name=node4_name,
                    value=top_level_unique_values_dict["7ad17f66-eec7-47e1-a367-131ccc0aabe9"],
                    initial_setup=True,
                    is_output=True,
                )
            )
        with GriptapeNodes.ContextManager().node(node5_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="model",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["0215b164-6a8d-443b-a066-e5bd7cfa86da"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="images",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["2bd3049f-84fe-4a9a-810b-7803f22275f7"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="size",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["ce0d0075-832d-420e-8525-d7c4fc193e8a"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="seed",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["91bd1e20-dfcd-44c4-a82a-8fae1ba78a93"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="max_images",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["dbe9a2ba-3a67-46c9-8e4e-eefe39a9f59e"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="guidance_scale",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["0e3eb9b7-3130-4abe-8521-0c1f25cefe12"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["f0f4b64d-3a1d-431a-9835-0a905bf437c4"],
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
                "executable": False,
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
                value=top_level_unique_values_dict["191c2c93-16af-4775-8d24-3ba10465028b"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items",
                node_name=node1_name,
                value=top_level_unique_values_dict["01f74ed5-692f-4b67-8088-a00d09a1c9c1"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_f21334b88f9248b5928497c8de05e92c",
                node_name=node1_name,
                value=top_level_unique_values_dict["c4511fea-ce0e-4134-958a-e42fc7437beb"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_3ca5b9e3ba9a40bc879ee4df68c7929d",
                node_name=node1_name,
                value=top_level_unique_values_dict["754a09d5-7e1a-4316-b6e9-abdbec93a19d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_e525d5d0e55240498d370869f6cd03df",
                node_name=node1_name,
                value=top_level_unique_values_dict["c484f041-778d-4a14-ac2e-43ffdf97441c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node1_name,
                value=top_level_unique_values_dict["ccdc067e-fe0c-4256-9e98-d56282ebd512"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node1_name,
                value=top_level_unique_values_dict["ccdc067e-fe0c-4256-9e98-d56282ebd512"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="layout_style",
                node_name=node2_name,
                value=top_level_unique_values_dict["1a7c93fb-6c9b-45fe-a297-388c4b9762ec"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="grid_justification",
                node_name=node2_name,
                value=top_level_unique_values_dict["7f11c6e4-e28f-4a11-a7bb-8c2fb225fecf"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="columns",
                node_name=node2_name,
                value=top_level_unique_values_dict["c85e10f2-2b29-40b5-9048-e244b3bb3f14"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="spacing",
                node_name=node2_name,
                value=top_level_unique_values_dict["46367adf-a58a-4aa9-a000-37e7df536672"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="border_radius",
                node_name=node2_name,
                value=top_level_unique_values_dict["4aba6118-4a31-4826-a73b-f44005594bc7"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="crop_to_fit",
                node_name=node2_name,
                value=top_level_unique_values_dict["6cdeb7d5-004a-44d0-af72-add3c028df0f"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="transparent_bg",
                node_name=node2_name,
                value=top_level_unique_values_dict["c4c4ae90-8152-491e-ab29-b71de163b4d5"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="background_color",
                node_name=node2_name,
                value=top_level_unique_values_dict["106aded4-a2c9-4a87-9d26-f1369305bdd5"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_image_size",
                node_name=node2_name,
                value=top_level_unique_values_dict["ef984dcd-d810-40f3-a8f9-1ea22e784962"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_preset",
                node_name=node2_name,
                value=top_level_unique_values_dict["b1310837-09a7-4258-814b-31ac2d957a38"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_image_width",
                node_name=node2_name,
                value=top_level_unique_values_dict["8bd0a338-b7b2-414c-bfbd-53c3ccd88d33"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_format",
                node_name=node2_name,
                value=top_level_unique_values_dict["7ab23d00-696f-49ac-a33a-8942e989ede8"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node2_name,
                value=top_level_unique_values_dict["51285cec-f932-4d1c-ad5c-ef2556659495"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node6_name,
                value=top_level_unique_values_dict["89f439c0-9eaa-4895-8d71-c8ddf196f31e"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node6_name,
                value=top_level_unique_values_dict["52a0e100-c349-47b4-a7a1-d7a4c2200372"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node6_name,
                value=top_level_unique_values_dict["5e77136a-d81e-4725-a665-9494effd2b87"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_input_paths",
                node_name=node6_name,
                value=top_level_unique_values_dict["3bda9f4e-c485-442f-b14d-f21d306ac2f5"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_output_paths",
                node_name=node6_name,
                value=top_level_unique_values_dict["e99a54da-23ab-4c95-9da5-772b578fee3a"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_priority",
                node_name=node6_name,
                value=top_level_unique_values_dict["58c7f348-9d4a-43b6-bbf8-d7b0b7d698b2"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_initial_state",
                node_name=node6_name,
                value=top_level_unique_values_dict["54dba5b3-700f-42bf-9b14-6c45e5a99d04"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node6_name,
                value=top_level_unique_values_dict["a3c27e7b-6c10-49c8-bcc7-c0a92479bda2"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node6_name,
                value=top_level_unique_values_dict["a3c27e7b-6c10-49c8-bcc7-c0a92479bda2"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_channels",
                node_name=node6_name,
                value=top_level_unique_values_dict["fb67b4ed-a502-4b29-8081-cbff0537b0e2"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_packages",
                node_name=node6_name,
                value=top_level_unique_values_dict["59a94ea3-185d-4185-9bb6-79482a1d900f"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_run_on_all_worker_hosts",
                node_name=node6_name,
                value=top_level_unique_values_dict["6cdeb7d5-004a-44d0-af72-add3c028df0f"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items",
                node_name=node6_name,
                value=top_level_unique_values_dict["ccdc067e-fe0c-4256-9e98-d56282ebd512"],
                initial_setup=True,
                is_output=False,
            )
        )
