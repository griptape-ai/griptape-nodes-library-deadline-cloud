# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_wedge_test"
# description = "An example demonstrating how a wedge test workflow can be triggered with parallel executions running as Jobs on AWS Deadline Cloud."
# schema_version = "0.13.0"
# engine_version_created_with = "0.64.1"
# node_libraries_referenced = [["Griptape Nodes Library", "0.51.1"]]
# node_types_used = [["Griptape Nodes Library", "CreateTextList"], ["Griptape Nodes Library", "DisplayImageGrid"], ["Griptape Nodes Library", "ForEachEndNode"], ["Griptape Nodes Library", "ForEachStartNode"], ["Griptape Nodes Library", "MergeTexts"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "SeedreamImageGeneration"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-11-27T01:29:09.358697Z
# last_modified_date = 2025-11-27T01:48:39.883690Z
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
    "f5604277-64d3-4549-942e-34467fdc3058": pickle.loads(
        b'\x80\x04\x95"\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x08Capybara\x94\x8c\x07Giraffe\x94\x8c\x05Zebra\x94e.'
    ),
    "2354acda-3a34-4766-8bc9-7f0b6f5b9556": pickle.loads(b"\x80\x04\x88."),
    "05df1ce6-fca5-467a-8d96-7ec55e75be30": pickle.loads(b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00]\x94(NNNe."),
    "4e8b040e-d2fc-460f-9af5-7a3f3bd8fe2a": pickle.loads(
        b'\x80\x04\x95"\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x08Capybara\x94\x8c\x07Giraffe\x94\x8c\x05Zebra\x94e.'
    ),
    "a84d6088-4430-4f16-9a39-d3fe77dfa9c0": pickle.loads(
        b"\x80\x04\x95\x0c\x00\x00\x00\x00\x00\x00\x00\x8c\x08Capybara\x94."
    ),
    "8f2921b2-dd04-4590-bf98-fecb48c49324": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07Giraffe\x94."
    ),
    "8f58007c-4b37-45cf-b46b-4cafd624fb86": pickle.loads(
        b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05Zebra\x94."
    ),
    "58de7ce2-04ee-407d-861f-c61435238010": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "19144714-7b20-4cb0-af66-8d50537eca75": pickle.loads(b"\x80\x04\x89."),
    "0643e454-9ddf-481e-88e8-74ff19e43990": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "839d2d40-5fdb-4e72-bb36-1802c4011206": pickle.loads(
        b"\x80\x04\x95\x0e\x00\x00\x00\x00\x00\x00\x00\x8c\nWedge Test\x94."
    ),
    "eb66ea93-76d4-472d-875a-d26d09d66f7c": pickle.loads(b"\x80\x04]\x94."),
    "002405c8-a56b-4fa9-907e-5d9e76cfece5": pickle.loads(b"\x80\x04]\x94."),
    "8cd47ff1-d067-438d-9e05-533952f8a967": pickle.loads(b"\x80\x04K2."),
    "4b5f53f3-edc3-4ede-953d-975eb1c0ea03": pickle.loads(
        b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05READY\x94."
    ),
    "b5dc9b6b-cf4b-423e-8a8f-79b4b12c326f": pickle.loads(b"\x80\x04K\x00."),
    "26fe8786-33ba-491b-b264-67da4c6cc6f2": pickle.loads(b"\x80\x04K\n."),
    "633cd2a5-7f0a-408b-8814-28ac043e8709": pickle.loads(
        b"\x80\x04\x95)\x00\x00\x00\x00\x00\x00\x00\x8c%farm-7bbde5411d444d039f12b30e007658fd\x94."
    ),
    "954f91bb-ab2b-401d-9474-c437d4452b3b": pickle.loads(
        b"\x80\x04\x95*\x00\x00\x00\x00\x00\x00\x00\x8c&queue-1c93aa55070f44279d03ed7a13918099\x94."
    ),
    "2bd304cd-35c3-46bf-a847-c6b5d5d13b47": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bconda-forge\x94."
    ),
    "7a56b3fa-9920-4c79-87e2-f94be31db6f5": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bpython=3.12\x94."
    ),
    "f5c0d737-7bf3-4f50-943a-d40f4683cf4b": pickle.loads(b"\x80\x04]\x94."),
    "d7550c84-adf4-4490-9f83-94975ec24fdb": pickle.loads(b"\x80\x04]\x94."),
    "845e2fb6-c522-40a8-954d-b943d813c680": pickle.loads(
        b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x0cseedream-4.0\x94."
    ),
    "82324c57-1a87-4b49-b044-dddc81f73abe": pickle.loads(
        b"\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00\x8c\x021K\x94."
    ),
    "df9708d6-8489-4e81-8595-ec32ee8265d4": pickle.loads(
        b"\x80\x04\x950\x00\x00\x00\x00\x00\x00\x00\x8c,<Results will appear when the node executes>\x94."
    ),
    "2e077556-6949-4d85-b17e-49c8aca40d4e": pickle.loads(
        b"\x80\x04\x95S\x01\x00\x00\x00\x00\x00\x00XL\x01\x00\x00# Overview\n\nExecuting this workflow will result in the below NodeGroup being published to AWS Deadline Cloud, and submitting 3 jobs in parallel to generate images for all 3 of the input subjects.\n\nThe ForEach nodes are used to iterate over the input list, and the NodeGroup specifies the execution environment of AWS Deadline Cloud.\x94."
    ),
}

"# Create the Flow, then do work within it as context."

flow0_name = GriptapeNodes.handle_request(
    CreateFlowRequest(parent_flow_name=None, set_as_new_context=False, metadata={})
).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="ForEachStartNode",
            specific_library_name="Griptape Nodes Library",
            node_name="ForEach Start",
            metadata={
                "position": {"x": 246.66666666666663, "y": 568.3333333333334},
                "tempId": "placing-1764206686171-g6fgpo",
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
                "size": {"width": 600, "height": 943},
                "category": "execution_flow",
            },
            resolution="resolved",
            initial_setup=True,
        )
    ).node_name
    node1_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="ForEachEndNode",
            specific_library_name="Griptape Nodes Library",
            node_name="ForEach End",
            metadata={
                "position": {"x": 3055.527727758382, "y": 568.3333333333334},
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
            resolution="resolved",
            initial_setup=True,
        )
    ).node_name
    node2_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="CreateTextList",
            specific_library_name="Griptape Nodes Library",
            node_name="Create Text List",
            metadata={
                "position": {"x": -868.9109320648583, "y": 850.0712224548605},
                "tempId": "placing-1764206716172-gek4vd4",
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
                "size": {"width": 710, "height": 618},
                "category": "lists",
            },
            resolution="resolved",
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="items_ParameterListUniqueParamID_b365f8bdec9b42168a724545bf71d9d9",
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
                parameter_name="items_ParameterListUniqueParamID_2752f1d679af489786f0b286b1e46436",
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
                parameter_name="items_ParameterListUniqueParamID_bee44f347f734a5598473ec3dded201b",
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
            node_type="MergeTexts",
            specific_library_name="Griptape Nodes Library",
            node_name="Merge Texts",
            metadata={
                "position": {"x": 78.42686690144751, "y": 138},
                "tempId": "placing-1764206770509-glbti",
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
                "size": {"width": 706, "height": 730},
                "category": "text",
                "empty_merge_string_migrated": True,
            },
            initial_setup=True,
        )
    ).node_name
    node4_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="SeedreamImageGeneration",
            specific_library_name="Griptape Nodes Library",
            node_name="Seedream Image Generation",
            metadata={
                "library_node_metadata": {
                    "category": "image",
                    "description": "Generate images using Seedream models (seedream-4.0, seedream-3.0-t2i) via Griptape model proxy",
                },
                "library": "Griptape Nodes Library",
                "node_type": "SeedreamImageGeneration",
                "position": {"x": 981.8083151002818, "y": 138.9544629035414},
                "size": {"width": 600, "height": 699},
                "showaddparameter": False,
                "category": "image",
            },
            initial_setup=True,
        )
    ).node_name
    node5_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DisplayImageGrid",
            specific_library_name="Griptape Nodes Library",
            node_name="Display Image Grid",
            metadata={
                "position": {"x": 3989.95338655045, "y": 568.3333333333334},
                "tempId": "placing-1764207939420-wg0fsm",
                "library_node_metadata": {
                    "category": "image",
                    "description": "Display multiple images in a grid or masonry layout with customizable styling options",
                },
                "library": "Griptape Nodes Library",
                "node_type": "DisplayImageGrid",
                "showaddparameter": False,
                "size": {"width": 1100, "height": 1208},
                "category": "image",
            },
            initial_setup=True,
        )
    ).node_name
    node6_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Note",
            metadata={
                "position": {"x": 1058.8814996314939, "y": -81.42865361426976},
                "tempId": "placing-1764207985055-1pqhx",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "size": {"width": 1738, "height": 603},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    node7_name = GriptapeNodes.handle_request(
        CreateNodeGroupRequest(
            node_group_name="NodeGroup",
            metadata={
                "position": {"x": 1034.9802947072883, "y": 627.6555234486176},
                "size": {"width": 1772, "height": 918},
                "node_type": "NodeGroupNode",
                "execution_environment": {
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
                "expanded_dimensions": {"width": 1772, "height": 918},
            },
            node_names_to_add=[node3_name, node4_name],
        )
    ).node_group_name
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
            source_node_name=node3_name,
            source_parameter_name="output",
            target_node_name=node4_name,
            target_parameter_name="prompt",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node3_name,
            source_parameter_name="exec_out",
            target_node_name=node4_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node4_name,
            source_parameter_name="exec_out",
            target_node_name=node1_name,
            target_parameter_name="add_item",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node4_name,
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
            target_node_name=node5_name,
            target_parameter_name="images",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node1_name,
            source_parameter_name="exec_out",
            target_node_name=node5_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items",
                node_name=node0_name,
                value=top_level_unique_values_dict["f5604277-64d3-4549-942e-34467fdc3058"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="run_in_parallel",
                node_name=node0_name,
                value=top_level_unique_values_dict["2354acda-3a34-4766-8bc9-7f0b6f5b9556"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="results",
                node_name=node1_name,
                value=top_level_unique_values_dict["05df1ce6-fca5-467a-8d96-7ec55e75be30"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items",
                node_name=node2_name,
                value=top_level_unique_values_dict["4e8b040e-d2fc-460f-9af5-7a3f3bd8fe2a"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_b365f8bdec9b42168a724545bf71d9d9",
                node_name=node2_name,
                value=top_level_unique_values_dict["a84d6088-4430-4f16-9a39-d3fe77dfa9c0"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_2752f1d679af489786f0b286b1e46436",
                node_name=node2_name,
                value=top_level_unique_values_dict["8f2921b2-dd04-4590-bf98-fecb48c49324"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="items_ParameterListUniqueParamID_bee44f347f734a5598473ec3dded201b",
                node_name=node2_name,
                value=top_level_unique_values_dict["8f58007c-4b37-45cf-b46b-4cafd624fb86"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node2_name,
                value=top_level_unique_values_dict["f5604277-64d3-4549-942e-34467fdc3058"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node2_name,
                value=top_level_unique_values_dict["f5604277-64d3-4549-942e-34467fdc3058"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_1",
                node_name=node3_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_2",
                node_name=node3_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_3",
                node_name=node3_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_4",
                node_name=node3_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="merge_string",
                node_name=node3_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="whitespace",
                node_name=node3_name,
                value=top_level_unique_values_dict["19144714-7b20-4cb0-af66-8d50537eca75"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node3_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node7_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node7_name,
                value=top_level_unique_values_dict["0643e454-9ddf-481e-88e8-74ff19e43990"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node7_name,
                value=top_level_unique_values_dict["0643e454-9ddf-481e-88e8-74ff19e43990"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="griptapecloudstartflow_enable_webhook_integration",
                node_name=node7_name,
                value=top_level_unique_values_dict["19144714-7b20-4cb0-af66-8d50537eca75"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="griptapecloudstartflow_enable_webhook_integration",
                node_name=node7_name,
                value=top_level_unique_values_dict["19144714-7b20-4cb0-af66-8d50537eca75"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node7_name,
                value=top_level_unique_values_dict["839d2d40-5fdb-4e72-bb36-1802c4011206"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node7_name,
                value=top_level_unique_values_dict["839d2d40-5fdb-4e72-bb36-1802c4011206"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node7_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node7_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_input_paths",
                node_name=node7_name,
                value=top_level_unique_values_dict["eb66ea93-76d4-472d-875a-d26d09d66f7c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_input_paths",
                node_name=node7_name,
                value=top_level_unique_values_dict["eb66ea93-76d4-472d-875a-d26d09d66f7c"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_output_paths",
                node_name=node7_name,
                value=top_level_unique_values_dict["002405c8-a56b-4fa9-907e-5d9e76cfece5"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_output_paths",
                node_name=node7_name,
                value=top_level_unique_values_dict["002405c8-a56b-4fa9-907e-5d9e76cfece5"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_priority",
                node_name=node7_name,
                value=top_level_unique_values_dict["8cd47ff1-d067-438d-9e05-533952f8a967"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_priority",
                node_name=node7_name,
                value=top_level_unique_values_dict["8cd47ff1-d067-438d-9e05-533952f8a967"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_initial_state",
                node_name=node7_name,
                value=top_level_unique_values_dict["4b5f53f3-edc3-4ede-953d-975eb1c0ea03"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_initial_state",
                node_name=node7_name,
                value=top_level_unique_values_dict["4b5f53f3-edc3-4ede-953d-975eb1c0ea03"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node7_name,
                value=top_level_unique_values_dict["b5dc9b6b-cf4b-423e-8a8f-79b4b12c326f"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node7_name,
                value=top_level_unique_values_dict["8cd47ff1-d067-438d-9e05-533952f8a967"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node7_name,
                value=top_level_unique_values_dict["b5dc9b6b-cf4b-423e-8a8f-79b4b12c326f"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node7_name,
                value=top_level_unique_values_dict["26fe8786-33ba-491b-b264-67da4c6cc6f2"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_farm_id",
                node_name=node7_name,
                value=top_level_unique_values_dict["633cd2a5-7f0a-408b-8814-28ac043e8709"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_farm_id",
                node_name=node7_name,
                value=top_level_unique_values_dict["633cd2a5-7f0a-408b-8814-28ac043e8709"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_queue_id",
                node_name=node7_name,
                value=top_level_unique_values_dict["954f91bb-ab2b-401d-9474-c437d4452b3b"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_queue_id",
                node_name=node7_name,
                value=top_level_unique_values_dict["954f91bb-ab2b-401d-9474-c437d4452b3b"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_storage_profile_id",
                node_name=node7_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_channels",
                node_name=node7_name,
                value=top_level_unique_values_dict["2bd304cd-35c3-46bf-a847-c6b5d5d13b47"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_channels",
                node_name=node7_name,
                value=top_level_unique_values_dict["2bd304cd-35c3-46bf-a847-c6b5d5d13b47"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_packages",
                node_name=node7_name,
                value=top_level_unique_values_dict["7a56b3fa-9920-4c79-87e2-f94be31db6f5"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_packages",
                node_name=node7_name,
                value=top_level_unique_values_dict["7a56b3fa-9920-4c79-87e2-f94be31db6f5"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_run_on_all_worker_hosts",
                node_name=node7_name,
                value=top_level_unique_values_dict["2354acda-3a34-4766-8bc9-7f0b6f5b9556"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_run_on_all_worker_hosts",
                node_name=node7_name,
                value=top_level_unique_values_dict["2354acda-3a34-4766-8bc9-7f0b6f5b9556"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_operating_system",
                node_name=node7_name,
                value=top_level_unique_values_dict["f5c0d737-7bf3-4f50-943a-d40f4683cf4b"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_cpu_architecture",
                node_name=node7_name,
                value=top_level_unique_values_dict["d7550c84-adf4-4490-9f83-94975ec24fdb"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="model",
                node_name=node4_name,
                value=top_level_unique_values_dict["845e2fb6-c522-40a8-954d-b943d813c680"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="prompt",
                node_name=node4_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="prompt",
                node_name=node4_name,
                value=top_level_unique_values_dict["58de7ce2-04ee-407d-861f-c61435238010"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="size",
                node_name=node4_name,
                value=top_level_unique_values_dict["82324c57-1a87-4b49-b044-dddc81f73abe"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node4_name,
                value=top_level_unique_values_dict["19144714-7b20-4cb0-af66-8d50537eca75"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node4_name,
                value=top_level_unique_values_dict["19144714-7b20-4cb0-af66-8d50537eca75"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node4_name,
                value=top_level_unique_values_dict["df9708d6-8489-4e81-8595-ec32ee8265d4"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node4_name,
                value=top_level_unique_values_dict["df9708d6-8489-4e81-8595-ec32ee8265d4"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node5_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="images",
                node_name=node5_name,
                value=top_level_unique_values_dict["05df1ce6-fca5-467a-8d96-7ec55e75be30"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node6_name,
                value=top_level_unique_values_dict["2e077556-6949-4d85-b17e-49c8aca40d4e"],
                initial_setup=True,
                is_output=False,
            )
        )
