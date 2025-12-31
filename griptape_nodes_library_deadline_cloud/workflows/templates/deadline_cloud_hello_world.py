# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_hello_world"
# schema_version = "0.14.0"
# engine_version_created_with = "0.66.2""
# node_libraries_referenced = [["Griptape Nodes Library", "0.55.0"], ["AWS Deadline Cloud Library", "0.66.2""]]
# node_types_used = [["Griptape Nodes Library", "AddTextToImage"], ["Griptape Nodes Library", "DisplayImage"], ["Griptape Nodes Library", "DisplayText"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "StandardSubflowNodeGroup"], ["Griptape Nodes Library", "TextInput"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-12-31T19:14:11.524832Z
# last_modified_date = 2025-12-31T19:14:11.756299Z
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
    "631d006a-d2dc-4cc6-bfbf-14412e102280": pickle.loads(b"\x80\x04K\x00."),
    "75e251fa-7435-4613-b654-3106171fc39c": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "455653fa-2578-4035-a9f4-ccc1760f4772": pickle.loads(
        b"\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rHello, world!\x94."
    ),
    "e87e3c28-3f08-4dc7-8347-f7f7b5ac2d49": pickle.loads(
        b"\x80\x04\x95\xb6\x00\x00\x00\x00\x00\x00\x00\x8c\xb2This workflow demonstrates a simple \"hello world\" example for confirming AWS Deadline Cloud functionality is working as expected.\n\nClick 'Run Workflow' to kick off the execution.\x94."
    ),
    "bce31966-80a9-48cb-83f3-9764844d7c91": pickle.loads(
        b"\x80\x04\x95p\x00\x00\x00\x00\x00\x00\x00\x8clThis is the happy path, indicating success. Your image will appear if Deadline Cloud completes successfully.\x94."
    ),
    "959f0810-81c1-42fb-8d42-4bc4c519461b": pickle.loads(
        b"\x80\x04\x95\x84\x00\x00\x00\x00\x00\x00\x00\x8c\x80If execution in Deadline Cloud fails, this path will be executed. The Display Text will provide information about what occurred.\x94."
    ),
    "fa23a2d1-c1c5-4ddb-8283-0067ee1b4d80": pickle.loads(
        b"\x80\x04\x95!\x01\x00\x00\x00\x00\x00\x00X\x1a\x01\x00\x00This node will be executed on Deadline Cloud.\n\nThe Subflow Node Group settings can be configured to specify an execution_environment of `AWS Deadline Cloud Library`, which indicates that all Nodes within the group should be packaged and shipped up to Deadline Cloud to run as a Job.\x94."
    ),
    "0e652ca0-e70d-41e4-868c-28331ff6e365": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "932a65b7-558b-45ec-a9fb-1462f679d933": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bHello World\x94."
    ),
    "bf28da47-a8a2-4ddf-84c0-4830cd1562cb": pickle.loads(
        b'\x80\x04\x95j\x00\x00\x00\x00\x00\x00\x00\x8cfA simple "hello world" example for confirming AWS Deadline Cloud functionality is working as expected.\x94.'
    ),
    "a1254298-c795-41a5-a36c-f21f2954186b": pickle.loads(b"\x80\x04]\x94."),
    "917616e7-e8d8-4bbc-99ff-7657dc73e044": pickle.loads(b"\x80\x04]\x94."),
    "9c3950e8-b6bc-4d20-8064-278ac956888b": pickle.loads(b"\x80\x04K2."),
    "5a4f61d5-a9f3-4a01-be6f-aec34126bd42": pickle.loads(
        b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05READY\x94."
    ),
    "7dca05e6-f818-43a2-8498-6ac31b873082": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bconda-forge\x94."
    ),
    "41fa1a97-f69d-4955-9b3a-b3e3c0bb1995": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bpython=3.12\x94."
    ),
    "fac95e87-10f9-4ae8-b219-8f797b5aeaa2": pickle.loads(b"\x80\x04\x88."),
    "146db54a-df58-42b5-ad12-fa06e5137ded": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\x00\x02."),
    "ca7da73c-1b70-4663-8e5f-3a5ed3b02a2a": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07#000080\x94."
    ),
    "93776d65-6f08-49d1-bcd9-f70973ae3944": pickle.loads(
        b"\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00\x8c\rHello, world!\x94."
    ),
    "14db75f6-1427-497c-b28f-9cd9611079dc": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07#00FFFF\x94."
    ),
    "55507b0a-bcad-4aa6-ac9f-8c242e91abf4": pickle.loads(b"\x80\x04K$."),
    "16644bec-a60f-4916-ba8e-d9a780825206": pickle.loads(b"\x80\x04\x89."),
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
                        display_name="Create Text Image",
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
                    value=top_level_unique_values_dict["146db54a-df58-42b5-ad12-fa06e5137ded"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="height",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["146db54a-df58-42b5-ad12-fa06e5137ded"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="background_color",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["ca7da73c-1b70-4663-8e5f-3a5ed3b02a2a"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="text",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["93776d65-6f08-49d1-bcd9-f70973ae3944"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="text_color",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["14db75f6-1427-497c-b28f-9cd9611079dc"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="font_size",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["55507b0a-bcad-4aa6-ac9f-8c242e91abf4"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["16644bec-a60f-4916-ba8e-d9a780825206"],
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
                "executable": True,
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
                value=top_level_unique_values_dict["631d006a-d2dc-4cc6-bfbf-14412e102280"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="width",
                node_name=node0_name,
                value=top_level_unique_values_dict["631d006a-d2dc-4cc6-bfbf-14412e102280"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="height",
                node_name=node0_name,
                value=top_level_unique_values_dict["631d006a-d2dc-4cc6-bfbf-14412e102280"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="height",
                node_name=node0_name,
                value=top_level_unique_values_dict["631d006a-d2dc-4cc6-bfbf-14412e102280"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node1_name,
                value=top_level_unique_values_dict["75e251fa-7435-4613-b654-3106171fc39c"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node2_name,
                value=top_level_unique_values_dict["455653fa-2578-4035-a9f4-ccc1760f4772"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node3_name,
                value=top_level_unique_values_dict["e87e3c28-3f08-4dc7-8347-f7f7b5ac2d49"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node4_name,
                value=top_level_unique_values_dict["bce31966-80a9-48cb-83f3-9764844d7c91"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node5_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node5_name,
                value=top_level_unique_values_dict["959f0810-81c1-42fb-8d42-4bc4c519461b"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node6_name,
                value=top_level_unique_values_dict["fa23a2d1-c1c5-4ddb-8283-0067ee1b4d80"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node8_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node8_name,
                value=top_level_unique_values_dict["0e652ca0-e70d-41e4-868c-28331ff6e365"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node8_name,
                value=top_level_unique_values_dict["932a65b7-558b-45ec-a9fb-1462f679d933"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node8_name,
                value=top_level_unique_values_dict["bf28da47-a8a2-4ddf-84c0-4830cd1562cb"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_input_paths",
                node_name=node8_name,
                value=top_level_unique_values_dict["a1254298-c795-41a5-a36c-f21f2954186b"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_output_paths",
                node_name=node8_name,
                value=top_level_unique_values_dict["917616e7-e8d8-4bbc-99ff-7657dc73e044"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_priority",
                node_name=node8_name,
                value=top_level_unique_values_dict["9c3950e8-b6bc-4d20-8064-278ac956888b"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_initial_state",
                node_name=node8_name,
                value=top_level_unique_values_dict["5a4f61d5-a9f3-4a01-be6f-aec34126bd42"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node8_name,
                value=top_level_unique_values_dict["631d006a-d2dc-4cc6-bfbf-14412e102280"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node8_name,
                value=top_level_unique_values_dict["631d006a-d2dc-4cc6-bfbf-14412e102280"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_storage_profile_id",
                node_name=node8_name,
                value=top_level_unique_values_dict["75e251fa-7435-4613-b654-3106171fc39c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_channels",
                node_name=node8_name,
                value=top_level_unique_values_dict["7dca05e6-f818-43a2-8498-6ac31b873082"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_packages",
                node_name=node8_name,
                value=top_level_unique_values_dict["41fa1a97-f69d-4955-9b3a-b3e3c0bb1995"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_run_on_all_worker_hosts",
                node_name=node8_name,
                value=top_level_unique_values_dict["fac95e87-10f9-4ae8-b219-8f797b5aeaa2"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="text",
                node_name=node8_name,
                value=top_level_unique_values_dict["455653fa-2578-4035-a9f4-ccc1760f4772"],
                initial_setup=True,
                is_output=False,
            )
        )
