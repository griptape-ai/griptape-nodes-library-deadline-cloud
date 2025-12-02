# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_wedge_test"
# description = "An example demonstrating how a wedge test workflow can be triggered with parallel executions running as Jobs on AWS Deadline Cloud."
# schema_version = "0.13.0"
# engine_version_created_with = "0.64.1"
# node_libraries_referenced = [["AWS Deadline Cloud Library", "0.64.1"], ["Griptape Nodes Library", "0.51.1"]]
# node_types_used = [["Griptape Nodes Library", "CreateTextList"], ["Griptape Nodes Library", "DisplayImageGrid"], ["Griptape Nodes Library", "ForEachEndNode"], ["Griptape Nodes Library", "ForEachStartNode"], ["Griptape Nodes Library", "MergeTexts"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "SeedreamImageGeneration"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-12-01T23:36:07.324516Z
# last_modified_date = 2025-12-01T23:41:32.636590Z
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
    "903c9a99-019f-4e9e-90f5-d7b89e4d9090": pickle.loads(
        b'\x80\x04\x95"\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x08Capybara\x94\x8c\x07Giraffe\x94\x8c\x05Zebra\x94e.'
    ),
    "7e3425c7-c468-464e-9173-9c68a179fd32": pickle.loads(b"\x80\x04\x88."),
    "f8446e91-9eec-4f5f-a48d-99f680c7a676": pickle.loads(
        b'\x80\x04\x95"\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x08Capybara\x94\x8c\x07Giraffe\x94\x8c\x05Zebra\x94e.'
    ),
    "55926661-b581-40a4-8d52-8ee8fb0c6227": pickle.loads(
        b"\x80\x04\x95\x0c\x00\x00\x00\x00\x00\x00\x00\x8c\x08Capybara\x94."
    ),
    "5d6a897e-a9da-45a2-9179-7af4133d27a6": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07Giraffe\x94."
    ),
    "8ab61ff2-8bfb-4d6d-9b48-2fe4eea82699": pickle.loads(
        b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05Zebra\x94."
    ),
    "899b0b98-76fb-48d9-be9e-ee487b0aee65": pickle.loads(b"\x80\x04K\x03."),
    "89eb7ac0-84ae-4df9-93e0-205fc40e19ad": pickle.loads(
        b"\x80\x04\x95S\x01\x00\x00\x00\x00\x00\x00XL\x01\x00\x00# Overview\n\nExecuting this workflow will result in the below NodeGroup being published to AWS Deadline Cloud, and submitting 3 jobs in parallel to generate images for all 3 of the input subjects.\n\nThe ForEach nodes are used to iterate over the input list, and the NodeGroup specifies the execution environment of AWS Deadline Cloud.\x94."
    ),
    "42e52454-9971-40d8-96f0-9e5aba32729b": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "7163e822-301f-47be-bdc2-6fa9270716bb": pickle.loads(
        b"\x80\x04\x95\x0e\x00\x00\x00\x00\x00\x00\x00\x8c\nWedge Test\x94."
    ),
    "bdbfa3be-85d3-4d71-b6bf-798e31c0cd21": pickle.loads(b"\x80\x04K\x00."),
    "10e760e5-5275-4b90-bd82-ef0b97296005": pickle.loads(
        b"\x80\x04\x95\x1b\x00\x00\x00\x00\x00\x00\x00\x8c\x17Generate an image of a:\x94."
    ),
    "45569706-5bab-4563-87dd-9b163190c364": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
}

"# Create the Flow, then do work within it as context."

flow0_name = GriptapeNodes.handle_request(
    CreateFlowRequest(parent_flow_name=None, flow_name="ControlFlow_1", set_as_new_context=False, metadata={})
).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="ForEachStartNode",
            specific_library_name="Griptape Nodes Library",
            node_name="ForEach Start",
            metadata={
                "position": {"x": 35.00000000000006, "y": 545},
                "tempId": "placing-1764631662906-7dmwtn",
                "library_node_metadata": NodeMetadata(
                    category="execution_flow",
                    description="Start node for iterating through a list of items and running a flow for each one",
                    display_name="ForEach Start",
                    tags=None,
                    icon="list-start",
                    color=None,
                    group="iteration",
                    deprecation=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "ForEachStartNode",
                "showaddparameter": False,
                "size": {"width": 601, "height": 726},
                "category": "execution_flow",
            },
            initial_setup=True,
        )
    ).node_name
    node1_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="ForEachEndNode",
            specific_library_name="Griptape Nodes Library",
            node_name="ForEach End",
            metadata={
                "position": {"x": 3469.693973097897, "y": 555.7455612458838},
                "library_node_metadata": NodeMetadata(
                    category="execution_flow",
                    description="End node that completes a loop iteration and connects back to the ForEachStartNode",
                    display_name="ForEach End",
                    tags=None,
                    icon="list-end",
                    color=None,
                    group="iteration",
                    deprecation=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "ForEachEndNode",
                "showaddparameter": False,
                "size": {"width": 600, "height": 372},
                "category": "execution_flow",
            },
            initial_setup=True,
        )
    ).node_name
    node2_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="CreateTextList",
            specific_library_name="Griptape Nodes Library",
            node_name="Create Text List",
            metadata={
                "position": {"x": -876.7604782945871, "y": 544.7455612458838},
                "tempId": "placing-1764631691360-l1vme",
                "library_node_metadata": NodeMetadata(
                    category="lists",
                    description="Creates a list of text items",
                    display_name="Create Text List",
                    tags=None,
                    icon=None,
                    color=None,
                    group="create",
                    deprecation=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "CreateTextList",
                "showaddparameter": False,
                "size": {"width": 665, "height": 713},
                "category": "lists",
            },
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="items_ParameterListUniqueParamID_295cf0052ad444438813c67cfdcb2b8c",
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
                parameter_name="items_ParameterListUniqueParamID_6d0b359ec0f0491c9831c9a62b7cfa0c",
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
                parameter_name="items_ParameterListUniqueParamID_1b8e83f01e7e40508c973b46f2417aee",
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
    node3_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DisplayImageGrid",
            specific_library_name="Griptape Nodes Library",
            node_name="Display Image Grid",
            metadata={
                "position": {"x": 4337.480914559839, "y": 555.7455612458838},
                "tempId": "placing-1764631982020-wj0lib",
                "library_node_metadata": NodeMetadata(
                    category="image",
                    description="Display multiple images in a grid or masonry layout with customizable styling options",
                    display_name="Display Image Grid",
                    tags=None,
                    icon="grid-3x3",
                    color=None,
                    group="display",
                    deprecation=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "DisplayImageGrid",
                "showaddparameter": False,
                "size": {"width": 1078, "height": 1090},
                "category": "image",
            },
            initial_setup=True,
        )
    ).node_name
    node4_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Wedge Test",
            metadata={
                "position": {"x": 1029.9178823800162, "y": 195.52798455245747},
                "tempId": "placing-1764632042919-u140k5",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "size": {"width": 2105, "height": 277},
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
        node5_name = GriptapeNodes.handle_request(
            CreateNodeRequest(
                node_type="MergeTexts",
                specific_library_name="Griptape Nodes Library",
                node_name="Merge Texts",
                metadata={
                    "position": {"x": 316, "y": 155},
                    "tempId": "placing-1764631761118-90txb7",
                    "library_node_metadata": NodeMetadata(
                        category="text",
                        description="MergeTexts node",
                        display_name="Merge Texts",
                        tags=None,
                        icon="merge",
                        color=None,
                        group="merge",
                        deprecation=None,
                    ),
                    "library": "Griptape Nodes Library",
                    "node_type": "MergeTexts",
                    "showaddparameter": False,
                    "size": {"width": 600, "height": 500},
                    "category": "text",
                },
                initial_setup=True,
            )
        ).node_name
        node6_name = GriptapeNodes.handle_request(
            CreateNodeRequest(
                node_type="SeedreamImageGeneration",
                specific_library_name="Griptape Nodes Library",
                node_name="Seedream Image Generation",
                metadata={
                    "position": {"x": 1096.687833773242, "y": 155},
                    "tempId": "placing-1764631793230-fwkwrl",
                    "library_node_metadata": NodeMetadata(
                        category="image",
                        description="Generate images using Seedream models (seedream-4.0, seedream-3.0-t2i) via Griptape model proxy",
                        display_name="Seedream Image Generation",
                        tags=None,
                        icon="Sparkles",
                        color=None,
                        group="create",
                        deprecation=None,
                    ),
                    "library": "Griptape Nodes Library",
                    "node_type": "SeedreamImageGeneration",
                    "showaddparameter": False,
                    "size": {"width": 600, "height": 884},
                    "category": "image",
                },
                initial_setup=True,
            )
        ).node_name
        GriptapeNodes.handle_request(
            CreateConnectionRequest(
                source_node_name=node5_name,
                source_parameter_name="output",
                target_node_name=node6_name,
                target_parameter_name="prompt",
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            CreateConnectionRequest(
                source_node_name=node5_name,
                source_parameter_name="exec_out",
                target_node_name=node6_name,
                target_parameter_name="exec_in",
                initial_setup=True,
            )
        )
        with GriptapeNodes.ContextManager().node(node5_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="input_1",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["10e760e5-5275-4b90-bd82-ef0b97296005"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="input_2",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["45569706-5bab-4563-87dd-9b163190c364"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["10e760e5-5275-4b90-bd82-ef0b97296005"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["10e760e5-5275-4b90-bd82-ef0b97296005"],
                    initial_setup=True,
                    is_output=True,
                )
            )
        with GriptapeNodes.ContextManager().node(node6_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="prompt",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["10e760e5-5275-4b90-bd82-ef0b97296005"],
                    initial_setup=True,
                    is_output=False,
                )
            )
    node7_name = GriptapeNodes.handle_request(
        CreateNodeGroupRequest(
            node_group_name="NodeGroup",
            metadata={
                "position": {"x": 1029.9178823800162, "y": 555.7455612458838},
                "size": {"width": 2119, "height": 1089},
                "node_type": "NodeGroupNode",
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
                },
                "subflow_name": "NodeGroup_subflow",
                "expanded_dimensions": {"width": 2119, "height": 1089},
                "left_parameters": ["exec_in", "input_2"],
                "right_parameters": ["exec_out", "image_url"],
            },
            node_names_to_add=[node5_name, node6_name],
        )
    ).node_group_name
    with GriptapeNodes.ContextManager().node(node7_name):
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
                parameter_name="input_2",
                tooltip="Enter any type of data for input_2.",
                type="any",
                input_types=["any"],
                output_type="any",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=True,
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="image_url",
                tooltip="Enter ImageUrlArtifact for image_url.",
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
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="loop",
            target_node_name=node1_name,
            target_parameter_name="from_start",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="loop_end_condition_met_signal",
            target_node_name=node1_name,
            target_parameter_name="loop_end_condition_met_signal_input",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node1_name,
            source_parameter_name="trigger_next_iteration_signal_output",
            target_node_name=node0_name,
            target_parameter_name="trigger_next_iteration_signal",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node1_name,
            source_parameter_name="break_loop_signal_output",
            target_node_name=node0_name,
            target_parameter_name="break_loop_signal",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node2_name,
            source_parameter_name="output",
            target_node_name=node0_name,
            target_parameter_name="items",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="exec_out",
            target_node_name=node7_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="exec_in",
            target_node_name=node5_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node6_name,
            source_parameter_name="exec_out",
            target_node_name=node7_name,
            target_parameter_name="exec_out",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="exec_out",
            target_node_name=node1_name,
            target_parameter_name="add_item",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="current_item",
            target_node_name=node7_name,
            target_parameter_name="input_2",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="input_2",
            target_node_name=node5_name,
            target_parameter_name="input_2",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node6_name,
            source_parameter_name="image_url",
            target_node_name=node7_name,
            target_parameter_name="image_url",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="image_url",
            target_node_name=node1_name,
            target_parameter_name="new_item_to_add",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node1_name,
            source_parameter_name="results",
            target_node_name=node3_name,
            target_parameter_name="images",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node1_name,
            source_parameter_name="exec_out",
            target_node_name=node3_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node2_name,
            source_parameter_name="exec_out",
            target_node_name=node0_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="output",
            target_node_name=node6_name,
            target_parameter_name="prompt",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="exec_out",
            target_node_name=node6_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="output",
            target_node_name=node6_name,
            target_parameter_name="prompt",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="exec_out",
            target_node_name=node6_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items",
                node_name=node0_name,
                value=top_level_unique_values_dict["903c9a99-019f-4e9e-90f5-d7b89e4d9090"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="run_in_parallel",
                node_name=node0_name,
                value=top_level_unique_values_dict["7e3425c7-c468-464e-9173-9c68a179fd32"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items",
                node_name=node2_name,
                value=top_level_unique_values_dict["f8446e91-9eec-4f5f-a48d-99f680c7a676"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_295cf0052ad444438813c67cfdcb2b8c",
                node_name=node2_name,
                value=top_level_unique_values_dict["55926661-b581-40a4-8d52-8ee8fb0c6227"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_6d0b359ec0f0491c9831c9a62b7cfa0c",
                node_name=node2_name,
                value=top_level_unique_values_dict["5d6a897e-a9da-45a2-9179-7af4133d27a6"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_1b8e83f01e7e40508c973b46f2417aee",
                node_name=node2_name,
                value=top_level_unique_values_dict["8ab61ff2-8bfb-4d6d-9b48-2fe4eea82699"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node2_name,
                value=top_level_unique_values_dict["903c9a99-019f-4e9e-90f5-d7b89e4d9090"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node2_name,
                value=top_level_unique_values_dict["903c9a99-019f-4e9e-90f5-d7b89e4d9090"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="columns",
                node_name=node3_name,
                value=top_level_unique_values_dict["899b0b98-76fb-48d9-be9e-ee487b0aee65"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node4_name,
                value=top_level_unique_values_dict["89eb7ac0-84ae-4df9-93e0-205fc40e19ad"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node7_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node7_name,
                value=top_level_unique_values_dict["42e52454-9971-40d8-96f0-9e5aba32729b"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node7_name,
                value=top_level_unique_values_dict["7163e822-301f-47be-bdc2-6fa9270716bb"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node7_name,
                value=top_level_unique_values_dict["bdbfa3be-85d3-4d71-b6bf-798e31c0cd21"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node7_name,
                value=top_level_unique_values_dict["bdbfa3be-85d3-4d71-b6bf-798e31c0cd21"],
                initial_setup=True,
                is_output=False,
            )
        )
