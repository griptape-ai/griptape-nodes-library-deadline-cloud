# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_hello_world"
# description = "A simple example demonstrating how a node can be tagged for execution on AWS Deadline Cloud within an existing workflow."
# schema_version = "0.14.0"
# engine_version_created_with = "0.64.1"
# node_libraries_referenced = [["AWS Deadline Cloud Library", "0.65.1"], ["Griptape Nodes Library", "0.52.2"]]
# node_types_used = [["Griptape Nodes Library", "AddTextToImage"], ["Griptape Nodes Library", "DisplayImage"], ["Griptape Nodes Library", "DisplayText"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "StandardSubflowNodeGroup"], ["Griptape Nodes Library", "TextInput"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-12-06T22:03:29.552501Z
# last_modified_date = 2025-12-06T22:03:31.614867Z
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
    "64fdd5e6-523d-4c9f-94be-23d8e534fc36": pickle.loads(b"\x80\x04K\x00."),
    "f332fa7d-df22-4720-a9f1-4a0ee839c79c": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "85f4f234-9e0b-4445-b268-385d9b950dcc": pickle.loads(
        b"\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rHello, world!\x94."
    ),
    "3860034f-8b7e-43fb-8a03-cd7546c15c46": pickle.loads(
        b'\x80\x04\x95\x85\x00\x00\x00\x00\x00\x00\x00\x8c\x81This workflow demonstrates a simple "hello world" example for confirming AWS Deadline Cloud functionality is working as expected.\x94.'
    ),
    "f309b9b3-789d-410e-b88f-64d882c46f1b": pickle.loads(
        b"\x80\x04\x95p\x00\x00\x00\x00\x00\x00\x00\x8clThis is the happy path, indicating success. Your image will appear if Deadline Cloud completes successfully.\x94."
    ),
    "70b61f80-92a1-49c1-bc04-1f67407619d1": pickle.loads(
        b"\x80\x04\x95\x84\x00\x00\x00\x00\x00\x00\x00\x8c\x80If execution in Deadline Cloud fails, this path will be executed. The Display Text will provide information about what occurred.\x94."
    ),
    "872019b9-e23a-47c4-9463-c4a09efd4383": pickle.loads(
        b"\x80\x04\x95!\x01\x00\x00\x00\x00\x00\x00X\x1a\x01\x00\x00This node will be executed on Deadline Cloud.\n\nThe Subflow Node Group settings can be configured to specify an execution_environment of `AWS Deadline Cloud Library`, which indicates that all Nodes within the group should be packaged and shipped up to Deadline Cloud to run as a Job.\x94."
    ),
    "01286aeb-afd1-4066-920d-d3b9e5047aed": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "a78acdf1-6a82-47f6-9f61-2c6b323ed54a": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bHello World\x94."
    ),
    "5e29cf31-5f58-48a6-9cf1-0643901316b8": pickle.loads(
        b'\x80\x04\x95j\x00\x00\x00\x00\x00\x00\x00\x8cfA simple "hello world" example for confirming AWS Deadline Cloud functionality is working as expected.\x94.'
    ),
    "25848860-7c0a-4122-8732-588127d638f2": pickle.loads(b"\x80\x04]\x94."),
    "3396427e-14f3-416d-867c-5fbecdb00ef9": pickle.loads(b"\x80\x04]\x94."),
    "a3469364-db49-40f1-a009-f5f92db13b60": pickle.loads(b"\x80\x04K2."),
    "fecda00a-5c4c-43e9-9416-02fba01c6727": pickle.loads(
        b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05READY\x94."
    ),
    "66130bfe-a8b3-4ae3-b8bd-88aed5648a25": pickle.loads(
        b"\x80\x04\x95)\x00\x00\x00\x00\x00\x00\x00\x8c%farm-7bbde5411d444d039f12b30e007658fd\x94."
    ),
    "b7b4ec8f-b301-43a9-b414-dfb41740cf02": pickle.loads(
        b"\x80\x04\x95*\x00\x00\x00\x00\x00\x00\x00\x8c&queue-1c93aa55070f44279d03ed7a13918099\x94."
    ),
    "fb9d33b5-7881-4ca0-8d7d-6ad787187733": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bconda-forge\x94."
    ),
    "356e280c-cff4-4de4-ac7a-45c17b970cb0": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bpython=3.12\x94."
    ),
    "90d9e388-a687-4a7a-bed7-ffa1f1dab2a3": pickle.loads(b"\x80\x04\x88."),
    "43bca9da-039e-49e6-8839-1c573dd4bedd": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\x00\x02."),
    "ef8ee304-bd44-4af1-8a29-9c330af91a0b": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07#000080\x94."
    ),
    "8e011cb8-fc6c-4ee7-ae7b-5551baa673c7": pickle.loads(
        b"\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rHello, world!\x94."
    ),
    "e45c04f0-be6e-4e05-bdd4-47af37ca6f13": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07#00FFFF\x94."
    ),
    "5aa8d498-004c-44b2-91fa-d526329f1f5e": pickle.loads(b"\x80\x04K$."),
    "894977c0-87ee-4cc2-816f-4a792f6e936c": pickle.loads(b"\x80\x04\x89."),
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
                "library_node_metadata": NodeMetadata(
                    category="image",
                    description="Display an image",
                    display_name="Display Image",
                    tags=None,
                    icon=None,
                    color=None,
                    group="display",
                    deprecation=None,
                    is_node_group=None,
                ),
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
                    is_node_group=None,
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
                "library_node_metadata": NodeMetadata(
                    category="text",
                    description="TextInput node",
                    display_name="Text Input",
                    tags=None,
                    icon="text-cursor",
                    color=None,
                    group="create",
                    deprecation=None,
                    is_node_group=None,
                ),
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
                "size": {"width": 1003, "height": 251},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    """# Create the Flow, then do work within it as context."""
    flow1_name = GriptapeNodes.handle_request(
        CreateFlowRequest(
            parent_flow_name=flow0_name,
            flow_name="Subflow Node Group_subflow",
            set_as_new_context=False,
            metadata={"flow_type": "NodeGroupFlow"},
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
                    "library_node_metadata": NodeMetadata(
                        category="image",
                        description="Create an image with text rendered on it",
                        display_name="Add Text to Image",
                        tags=None,
                        icon="Type",
                        color=None,
                        group="create",
                        deprecation=None,
                        is_node_group=None,
                    ),
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
                    parameter_name="width",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["43bca9da-039e-49e6-8839-1c573dd4bedd"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="height",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["43bca9da-039e-49e6-8839-1c573dd4bedd"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="background_color",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["ef8ee304-bd44-4af1-8a29-9c330af91a0b"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="text",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["8e011cb8-fc6c-4ee7-ae7b-5551baa673c7"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="text_color",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["e45c04f0-be6e-4e05-bdd4-47af37ca6f13"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="font_size",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["5aa8d498-004c-44b2-91fa-d526329f1f5e"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["894977c0-87ee-4cc2-816f-4a792f6e936c"],
                    initial_setup=True,
                    is_output=False,
                )
            )
    node8_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="StandardSubflowNodeGroup",
            specific_library_name="Griptape Nodes Library",
            node_name="Subflow Node Group",
            metadata={
                "position": {"x": 749.0223191048804, "y": 363.6283026876037},
                "size": {"width": 1015, "height": 1062},
                "library": "Griptape Nodes Library",
                "node_type": "StandardSubflowNodeGroup",
                "is_node_group": True,
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
                "subflow_name": "Subflow Node Group_subflow",
                "expanded_dimensions": {"width": 1015, "height": 1062},
                "left_parameters": ["exec_in", "text"],
                "right_parameters": ["exec_out", "image", "failure", "result_details"],
                "library_node_metadata": NodeMetadata(
                    category="execution_flow",
                    description="Groups multiple nodes together for organization and parallel execution",
                    display_name="Subflow Node Group",
                    tags=None,
                    icon="Layers",
                    color=None,
                    group=None,
                    deprecation=None,
                    is_node_group=True,
                ),
            },
            node_names_to_add=[node7_name],
        )
    ).node_name
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
                value=top_level_unique_values_dict["64fdd5e6-523d-4c9f-94be-23d8e534fc36"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="width",
                node_name=node0_name,
                value=top_level_unique_values_dict["64fdd5e6-523d-4c9f-94be-23d8e534fc36"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="height",
                node_name=node0_name,
                value=top_level_unique_values_dict["64fdd5e6-523d-4c9f-94be-23d8e534fc36"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="height",
                node_name=node0_name,
                value=top_level_unique_values_dict["64fdd5e6-523d-4c9f-94be-23d8e534fc36"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node1_name,
                value=top_level_unique_values_dict["f332fa7d-df22-4720-a9f1-4a0ee839c79c"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node2_name,
                value=top_level_unique_values_dict["85f4f234-9e0b-4445-b268-385d9b950dcc"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node3_name,
                value=top_level_unique_values_dict["3860034f-8b7e-43fb-8a03-cd7546c15c46"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node4_name,
                value=top_level_unique_values_dict["f309b9b3-789d-410e-b88f-64d882c46f1b"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node5_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node5_name,
                value=top_level_unique_values_dict["70b61f80-92a1-49c1-bc04-1f67407619d1"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node6_name,
                value=top_level_unique_values_dict["872019b9-e23a-47c4-9463-c4a09efd4383"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node8_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node8_name,
                value=top_level_unique_values_dict["01286aeb-afd1-4066-920d-d3b9e5047aed"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node8_name,
                value=top_level_unique_values_dict["a78acdf1-6a82-47f6-9f61-2c6b323ed54a"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node8_name,
                value=top_level_unique_values_dict["5e29cf31-5f58-48a6-9cf1-0643901316b8"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_input_paths",
                node_name=node8_name,
                value=top_level_unique_values_dict["25848860-7c0a-4122-8732-588127d638f2"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_output_paths",
                node_name=node8_name,
                value=top_level_unique_values_dict["3396427e-14f3-416d-867c-5fbecdb00ef9"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_priority",
                node_name=node8_name,
                value=top_level_unique_values_dict["a3469364-db49-40f1-a009-f5f92db13b60"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_initial_state",
                node_name=node8_name,
                value=top_level_unique_values_dict["fecda00a-5c4c-43e9-9416-02fba01c6727"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node8_name,
                value=top_level_unique_values_dict["64fdd5e6-523d-4c9f-94be-23d8e534fc36"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node8_name,
                value=top_level_unique_values_dict["64fdd5e6-523d-4c9f-94be-23d8e534fc36"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_farm_id",
                node_name=node8_name,
                value=top_level_unique_values_dict["66130bfe-a8b3-4ae3-b8bd-88aed5648a25"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_queue_id",
                node_name=node8_name,
                value=top_level_unique_values_dict["b7b4ec8f-b301-43a9-b414-dfb41740cf02"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_channels",
                node_name=node8_name,
                value=top_level_unique_values_dict["fb9d33b5-7881-4ca0-8d7d-6ad787187733"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_packages",
                node_name=node8_name,
                value=top_level_unique_values_dict["356e280c-cff4-4de4-ac7a-45c17b970cb0"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_run_on_all_worker_hosts",
                node_name=node8_name,
                value=top_level_unique_values_dict["90d9e388-a687-4a7a-bed7-ffa1f1dab2a3"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node8_name,
                value=top_level_unique_values_dict["85f4f234-9e0b-4445-b268-385d9b950dcc"],
                initial_setup=True,
                is_output=False,
            )
        )
