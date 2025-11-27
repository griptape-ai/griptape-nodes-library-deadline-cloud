# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_train_lora"
# description = "An example demonstrating how a NodeGroup can be used to send a LoRA training subflow up to AWS Deadline Cloud within a running workflow."
# schema_version = "0.13.0"
# engine_version_created_with = "0.64.1"
# node_libraries_referenced = [["Griptape Nodes Lora Training Library", "0.60.0"], ["Griptape Nodes Library", "0.51.1"]]
# node_types_used = [["Griptape Nodes Library", "EndFlow"], ["Griptape Nodes Library", "EngineNode"], ["Griptape Nodes Library", "MergeTexts"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "PathJoin"], ["Griptape Nodes Library", "StartFlow"], ["Griptape Nodes Lora Training Library", "DownloadDatasetNode"], ["Griptape Nodes Lora Training Library", "GenerateDatasetNode"], ["Griptape Nodes Lora Training Library", "TrainLoraNode"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-11-25T02:11:16.160411Z
# last_modified_date = 2025-11-27T01:01:04.045432Z
# workflow_shape = "{\"inputs\":{\"Start Flow\":{\"exec_out\":{\"name\":\"exec_out\",\"tooltip\":\"Connection to the next node in the execution chain\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Flow Out\"},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null}}},\"outputs\":{\"End Flow\":{\"exec_in\":{\"name\":\"exec_in\",\"tooltip\":\"Control path when the flow completed successfully\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Succeeded\"},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"failed\":{\"name\":\"failed\",\"tooltip\":\"Control path when the flow failed\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Failed\"},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"was_successful\":{\"name\":\"was_successful\",\"tooltip\":\"Indicates whether it completed without errors.\",\"type\":\"bool\",\"input_types\":[\"bool\"],\"output_type\":\"bool\",\"default_value\":false,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{},\"settable\":false,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"result_details\":{\"name\":\"result_details\",\"tooltip\":\"Details about the operation result\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"multiline\":true,\"placeholder_text\":\"Details about the completion or failure will be shown here.\"},\"settable\":false,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"output\":{\"name\":\"output\",\"tooltip\":\"New parameter\",\"type\":\"str\",\"input_types\":[\"any\"],\"output_type\":\"str\",\"default_value\":\"\",\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"multiline\":true,\"placeholder_text\":\"The merged text result.\",\"is_custom\":true,\"is_user_added\":true},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":\"\",\"parent_element_name\":null}}}}"
#
# ///

import argparse
import asyncio
import json
import pickle
from griptape_nodes.bootstrap.workflow_executors.local_workflow_executor import LocalWorkflowExecutor
from griptape_nodes.bootstrap.workflow_executors.workflow_executor import WorkflowExecutor
from griptape_nodes.drivers.storage.storage_backend import StorageBackend
from griptape_nodes.node_library.library_registry import IconVariant, NodeDeprecationMetadata, NodeMetadata
from griptape_nodes.retained_mode.events.connection_events import CreateConnectionRequest
from griptape_nodes.retained_mode.events.flow_events import (
    CreateFlowRequest,
    GetTopLevelFlowRequest,
    GetTopLevelFlowResultSuccess,
)
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
    context_manager.push_workflow(workflow_name="deadline_cloud_train_lora")

"""
1. We've collated all of the unique parameter values into a dictionary so that we do not have to duplicate them.
   This minimizes the size of the code, especially for large objects like serialized image files.
2. We're using a prefix so that it's clear which Flow these values are associated with.
3. The values are serialized using pickle, which is a binary format. This makes them harder to read, but makes
   them consistently save and load. It allows us to serialize complex objects like custom classes, which otherwise
   would be difficult to serialize.
"""
top_level_unique_values_dict = {
    "d9fd198a-766a-4115-bb62-2a22565f09bc": pickle.loads(
        b"\x80\x04\x95K\x00\x00\x00\x00\x00\x00\x00\x8cGhttps://griptape-cloud-assets.s3.amazonaws.com/dataSet_CHICKAPIGLET.zip\x94."
    ),
    "e08615e7-4771-4f51-a45d-87cfee557417": pickle.loads(
        b"\x80\x04\x95|\x00\x00\x00\x00\x00\x00\x00\x8cx/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10\x94."
    ),
    "a5ae06cd-cfac-4ec2-9fc4-02f435497a71": pickle.loads(
        b"\x80\x04\x95\x91\x00\x00\x00\x00\x00\x00\x00\x8c\x8d/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10/dataSet_CHICKAPIGLET\x94."
    ),
    "7a7077eb-9be3-424d-9b0c-e7cdf98b0843": pickle.loads(b"\x80\x04\x88."),
    "a162754b-2521-4706-ba45-41b0cff81738": pickle.loads(
        b"\x80\x04\x95\x19\x00\x00\x00\x00\x00\x00\x00\x8c\x15GetConfigValueRequest\x94."
    ),
    "849db959-99c5-4c4b-9f99-24bf48c0a492": pickle.loads(
        b"\x80\x04\x95[\x00\x00\x00\x00\x00\x00\x00\x8cWSUCCESS: [10] Successfully returned the config value for section 'workspace_directory'.\x94."
    ),
    "3c60b030-5c59-4de3-b738-698a9ea9ea17": pickle.loads(
        b"\x80\x04\x95\x17\x00\x00\x00\x00\x00\x00\x00\x8c\x13workspace_directory\x94."
    ),
    "8fe787b7-53e1-4bca-9f87-b1fa7f1216df": pickle.loads(
        b"\x80\x04\x95s\x00\x00\x00\x00\x00\x00\x00\x8coDescribe this image with descriptive tags. Include details about the subject, setting, colors, mood, and style.\x94."
    ),
    "6a12e799-13b0-4078-9ca8-a63009eecd28": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07cartoon\x94."
    ),
    "90d80844-07a6-4694-b3de-6e3c6e7d3c89": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\x00\x02."),
    "30d58adb-9b4d-4aea-a3a9-13ce909dfabf": pickle.loads(
        b"\x80\x04\x95\x9e\x00\x00\x00\x00\x00\x00\x00\x8c\x9a/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10/dataSet_CHICKAPIGLET/dataset.toml\x94."
    ),
    "ed84b3cc-8ae9-4682-ae84-febb81b41566": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07Success\x94."
    ),
    "fa4b5333-53bc-4239-bf30-29a9d22cedcb": pickle.loads(
        b"\x80\x04\x95\x1b\x00\x00\x00\x00\x00\x00\x00\x8c\x17Control Input Selection\x94."
    ),
    "39e9da79-e6d4-4de1-81f2-23e64a3b1127": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06FLUX.1\x94."
    ),
    "f904685f-4888-4bf1-848b-ce18ba8901e7": pickle.loads(
        b"\x80\x04\x95 \x00\x00\x00\x00\x00\x00\x00\x8c\x1cblack-forest-labs/FLUX.1-dev\x94."
    ),
    "5f643152-9c0b-459f-ac3a-ac554cb0de6c": pickle.loads(
        b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x0cmy_flux_lora\x94."
    ),
    "9c4412ac-7a99-47e1-8998-a4a2d076728f": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00G?J6\xe2\xeb\x1cC-."
    ),
    "6d5b7f06-00e2-4428-9a90-36b20925b79d": pickle.loads(b"\x80\x04K\x08."),
    "a86e110f-389b-436c-bef4-3e90136407c8": pickle.loads(b"\x80\x04K\x10."),
    "c02c3580-ebdf-4727-bc09-b38f704fea8e": pickle.loads(b"\x80\x04K\x04."),
    "c2d23049-58dc-4055-9ec0-252381272fd6": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04bf16\x94."
    ),
    "fb6fe015-0fd5-441d-b9b8-bf3b5eae8e98": pickle.loads(b"\x80\x04K\x02."),
    "5102ee0e-bf14-43b3-a05c-70efb5b61f02": pickle.loads(b"\x80\x04\x89."),
    "e875f66d-a41b-49c0-870f-52ae70767cef": pickle.loads(b"\x80\x04K*."),
    "00943df6-625b-4d77-baea-11352f999527": pickle.loads(
        b"\x80\x04\x951\x00\x00\x00\x00\x00\x00\x00\x8c-SUCCESS: LoRA training executed successfully.\x94."
    ),
    "e2838058-6692-457a-ba27-4cf61fc79570": pickle.loads(
        b"\x80\x04\x95\xd7\x00\x00\x00\x00\x00\x00\x00\x8c\xd3You can find your safetensor output file at: /tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_b39ejg7q/output/694d044bd3e04acdb467f5540857ffa5/dataSet_CHICKAPIGLET/my_flux_lora.safetensors\x94."
    ),
    "80527f3d-e8e1-4160-833f-e7c7c1075006": pickle.loads(
        b"\x80\x04\x95\xa4\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x8d/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_b39ejg7q/output/694d044bd3e04acdb467f5540857ffa5/dataSet_CHICKAPIGLET\x94\x8c\x0cmy_flux_lora\x94e."
    ),
    "3057e0e2-48f2-4175-b64d-9aa8aac730de": pickle.loads(
        b"\x80\x04\x95\x91\x00\x00\x00\x00\x00\x00\x00\x8c\x8d/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_b39ejg7q/output/694d044bd3e04acdb467f5540857ffa5/dataSet_CHICKAPIGLET\x94."
    ),
    "14fbd596-c47a-4947-9ae1-a53868e289e5": pickle.loads(
        b"\x80\x04\x95\x9e\x00\x00\x00\x00\x00\x00\x00\x8c\x9a/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_b39ejg7q/output/694d044bd3e04acdb467f5540857ffa5/dataSet_CHICKAPIGLET/my_flux_lora\x94."
    ),
    "558dbddd-d8e9-4461-926d-be96e591a374": pickle.loads(
        b"\x80\x04\x95/\x00\x00\x00\x00\x00\x00\x00\x8c+You can find your safetensor output file at\x94."
    ),
    "304a22a4-f82e-48c7-ae2d-c479b3ee861f": pickle.loads(
        b"\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00\x8c\x02: \x94."
    ),
    "b632dcfe-a3bb-4257-9ad8-b3aac6861166": pickle.loads(
        b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x0c.safetensors\x94."
    ),
    "c9be30c8-cf08-4bd7-9ac1-e2490cbe887e": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "5f93cb09-ba1c-44b0-a6e5-9c4fa4a28f10": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "1ca68a1b-3589-4c97-bb1e-54c4d372bc70": pickle.loads(
        b"\x80\x04\x95\x0e\x00\x00\x00\x00\x00\x00\x00\x8c\nTrain LoRA\x94."
    ),
    "e1180bcc-cbbf-491a-b58b-9b2287e45294": pickle.loads(
        b'\x80\x04\x95&\x00\x00\x00\x00\x00\x00\x00\x8c"Train a LoRA on AWS Deadline Cloud\x94.'
    ),
    "d500b9b0-93ba-47d3-af8c-e2e2babc904d": pickle.loads(b"\x80\x04K\x00."),
    "18f615a1-764e-4426-be51-f73771f08e94": pickle.loads(
        b"\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x03min\x94K\x01\x8c\x03max\x94K\x02u."
    ),
    "164b39cb-b634-4d93-8a56-f921467d95a0": pickle.loads(
        b"\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x03min\x94K\x00\x8c\x03max\x94K\x00u."
    ),
    "c014e143-757c-4afd-88a6-efa2937a4c43": pickle.loads(
        b"\x80\x04\x95\x9a\x03\x00\x00\x00\x00\x00\x00X\x93\x03\x00\x00# Overview\n\nThis workflow runs a LoRA Training process on AWS Deadline Cloud and returns the generated safetensors file.\n\n## Libraries\n\n* Griptape Nodes Standard Library: https://github.com/griptape-ai/griptape-nodes-library-standard\n* LoRA Training Library: https://github.com/griptape-ai/griptape-nodes-lora-training-library\n  * Note: Register the Library with the `griptape-nodes-library-cuda129.json` file for compatibility with Deadline\n* AWS Deadline Cloud Library: https://github.com/griptape-ai/griptape-nodes-library-deadline-cloud\n\n## NodeGroup\n\nAll of the Nodes in the below NodeGroup will be packaged and submitted to AWS Deadline Cloud as a Job. This will happen when the workflow runs. The output from the Job will include a safetensors file if the LoRA training was successful. The end of this workflow will display the file path location where the safetensors file was downloaded to on your machine.\x94."
    ),
}

"# Create the Flow, then do work within it as context."

flow0_name = GriptapeNodes.handle_request(
    CreateFlowRequest(parent_flow_name=None, set_as_new_context=False, metadata={})
).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="DownloadDatasetNode",
            specific_library_name="Griptape Nodes Lora Training Library",
            node_name="Download Dataset",
            metadata={
                "library_node_metadata": NodeMetadata(
                    category="lora",
                    description="Griptape Node that downloads and extracts a dataset zip from a URL.",
                    display_name="Download Dataset",
                    tags=None,
                    icon=None,
                    color=None,
                    group=None,
                    deprecation=None,
                ),
                "library": "Griptape Nodes Lora Training Library",
                "node_type": "DownloadDatasetNode",
                "position": {"x": 1251.8635317591663, "y": 354},
                "size": {"width": 902, "height": 884},
                "showaddparameter": False,
            },
            initial_setup=True,
        )
    ).node_name
    node1_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="EngineNode",
            specific_library_name="Griptape Nodes Library",
            node_name="Engine Node",
            metadata={
                "library_node_metadata": NodeMetadata(
                    category="engine",
                    description="Dynamically call any RequestPayload in the engine",
                    display_name="Engine Node",
                    tags=None,
                    icon="Cog",
                    color=None,
                    group=None,
                    deprecation=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "EngineNode",
                "position": {"x": 220.95540557790287, "y": 354},
                "size": {"width": 801, "height": 897},
                "showaddparameter": False,
                "category": "engine",
            },
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="input_category_and_key",
                tooltip="Input for category_and_key (type: str)",
                type="str",
                input_types=["str"],
                output_type="str",
                ui_options={"display_name": "category_and_key"},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=False,
                is_user_defined=True,
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="output_success_value",
                tooltip="Output from success result: value (type: all)",
                type="all",
                input_types=["all"],
                output_type="all",
                ui_options={"display_name": "value"},
                mode_allowed_input=False,
                mode_allowed_property=False,
                mode_allowed_output=True,
                is_user_defined=True,
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="output_failure_exception",
                tooltip="Output from failure result: exception (type: exception)",
                type="exception",
                input_types=["exception"],
                output_type="exception",
                ui_options={"display_name": "exception (optional)"},
                mode_allowed_input=False,
                mode_allowed_property=False,
                mode_allowed_output=True,
                is_user_defined=True,
                initial_setup=True,
            )
        )
    node2_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="GenerateDatasetNode",
            specific_library_name="Griptape Nodes Lora Training Library",
            node_name="Generate Lora Dataset",
            metadata={
                "position": {"x": 2292.7643205176246, "y": 354},
                "tempId": "placing-1764036163069-5xh83",
                "library_node_metadata": NodeMetadata(
                    category="lora",
                    description="Griptape Node that generates a dataset for LoRA training.",
                    display_name="Generate LoRA Dataset",
                    tags=None,
                    icon=None,
                    color=None,
                    group=None,
                    deprecation=None,
                ),
                "library": "Griptape Nodes Lora Training Library",
                "node_type": "GenerateDatasetNode",
                "showaddparameter": False,
                "size": {"width": 851, "height": 887},
                "category": "lora",
            },
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            AlterParameterDetailsRequest(parameter_name="agent", ui_options={"hide": False}, initial_setup=True)
        )
        GriptapeNodes.handle_request(
            AlterParameterDetailsRequest(
                parameter_name="agent_prompt", ui_options={"multiline": True, "hide": False}, initial_setup=True
            )
        )
        GriptapeNodes.handle_request(
            AlterParameterDetailsRequest(parameter_name="captions", ui_options={"hide": True}, initial_setup=True)
        )
    node3_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="TrainLoraNode",
            specific_library_name="Griptape Nodes Lora Training Library",
            node_name="Train Lora",
            metadata={
                "position": {"x": 3318.8608672706287, "y": 276.8559349073889},
                "tempId": "placing-1764036252451-zq6id8",
                "library_node_metadata": NodeMetadata(
                    category="lora",
                    description="Griptape Node that trains a LoRA model.",
                    display_name="Train LoRA",
                    tags=None,
                    icon=None,
                    color=None,
                    group=None,
                    deprecation=None,
                ),
                "library": "Griptape Nodes Lora Training Library",
                "node_type": "TrainLoraNode",
                "showaddparameter": False,
                "size": {"width": 1019, "height": 1072},
                "category": "lora",
            },
            initial_setup=True,
        )
    ).node_name
    node4_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="StartFlow",
            specific_library_name="Griptape Nodes Library",
            node_name="Start Flow",
            metadata={
                "position": {"x": -1188.4680657484485, "y": -1758.09940346112},
                "tempId": "placing-1764036813381-cun22",
                "library_node_metadata": {
                    "category": "workflows",
                    "description": "Define the start of a workflow and pass parameters into the flow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "StartFlow",
                "showaddparameter": True,
                "size": {"width": 932, "height": 1479},
                "category": "workflows",
            },
            resolution="resolved",
            initial_setup=True,
        )
    ).node_name
    node5_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="EndFlow",
            specific_library_name="Griptape Nodes Library",
            node_name="End Flow",
            metadata={
                "position": {"x": 7751.1778357033, "y": -1683.7637498379243},
                "tempId": "placing-1764036892906-ygdy5h",
                "library_node_metadata": NodeMetadata(
                    category="workflows",
                    description="Define the end of a workflow and return parameters from the flow",
                    display_name="End Flow",
                    tags=None,
                    icon=None,
                    color=None,
                    group="create",
                    deprecation=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "EndFlow",
                "showaddparameter": True,
                "size": {"width": 1298, "height": 1137},
                "category": "workflows",
            },
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node5_name):
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="output",
                default_value="",
                tooltip="New parameter",
                type="str",
                input_types=["any"],
                output_type="str",
                ui_options={
                    "multiline": True,
                    "placeholder_text": "The merged text result.",
                    "is_custom": True,
                    "is_user_added": True,
                },
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=True,
                parent_container_name="",
                initial_setup=True,
            )
        )
    node6_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="PathJoin",
            specific_library_name="Griptape Nodes Library",
            node_name="Path Join",
            metadata={
                "position": {"x": 5082.515361950617, "y": -1683.7637498379243},
                "tempId": "placing-1764203053587-o3fxlw",
                "library_node_metadata": NodeMetadata(
                    category="files",
                    description="Join multiple path components together to create a file path using appropriate path separators",
                    display_name="Path Join",
                    tags=None,
                    icon="Combine",
                    color=None,
                    group=None,
                    deprecation=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "PathJoin",
                "showaddparameter": False,
                "size": {"width": 1062, "height": 1293},
                "category": "files",
            },
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="path_components_ParameterListUniqueParamID_45408bf4aba54a9294b36238d61f9a2b",
                tooltip="Path components to join together.",
                type="str",
                input_types=["str"],
                output_type="str",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=False,
                is_user_defined=True,
                settable=True,
                parent_container_name="path_components",
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="path_components_ParameterListUniqueParamID_0023d659494d4111bef715fbbce4d573",
                tooltip="Path components to join together.",
                type="str",
                input_types=["str"],
                output_type="str",
                ui_options={},
                mode_allowed_input=True,
                mode_allowed_property=True,
                mode_allowed_output=False,
                is_user_defined=True,
                settable=True,
                parent_container_name="path_components",
                initial_setup=True,
            )
        )
    node7_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="MergeTexts",
            specific_library_name="Griptape Nodes Library",
            node_name="Merge Texts",
            metadata={
                "position": {"x": 6474.82534181051, "y": -1683.7637498379243},
                "tempId": "placing-1764203125886-o0tu1c",
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
                "size": {"width": 1072, "height": 1143},
                "category": "text",
                "empty_merge_string_migrated": True,
            },
            initial_setup=True,
        )
    ).node_name
    node8_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Note",
            metadata={
                "position": {"x": 47.63740729474671, "y": -2564.9737855651842},
                "tempId": "placing-1764204840994-phevm",
                "library_node_metadata": {
                    "category": "misc",
                    "description": "Create a note node to provide helpful context in your workflow",
                },
                "library": "Griptape Nodes Library",
                "node_type": "Note",
                "showaddparameter": False,
                "size": {"width": 1319, "height": 754},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    node9_name = GriptapeNodes.handle_request(
        CreateNodeGroupRequest(
            node_group_name="NodeGroup",
            metadata={
                "position": {"x": 47.63740729474671, "y": -1772.3333333333333},
                "size": {"width": 4569, "height": 1476},
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
                "expanded_dimensions": {"width": 4569, "height": 1476},
                "left_parameters": ["exec_in"],
                "right_parameters": ["exec_out"],
            },
            node_names_to_add=[node0_name, node1_name, node2_name, node3_name],
        )
    ).node_group_name
    with GriptapeNodes.ContextManager().node(node9_name):
        GriptapeNodes.handle_request(
            AlterParameterDetailsRequest(
                parameter_name="deadlinecloudstartflow_farm_id",
                ui_options={"simple_dropdown": ["None"], "show_search": True, "search_filter": ""},
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            AlterParameterDetailsRequest(
                parameter_name="deadlinecloudstartflow_queue_id",
                ui_options={"simple_dropdown": ["None"], "show_search": True, "search_filter": ""},
                initial_setup=True,
            )
        )
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
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="extracted_path",
            target_node_name=node2_name,
            target_parameter_name="dataset_folder",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node2_name,
            source_parameter_name="dataset_config_path",
            target_node_name=node3_name,
            target_parameter_name="dataset_config_path",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node1_name,
            source_parameter_name="output_success_value",
            target_node_name=node0_name,
            target_parameter_name="extract_location",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
            source_parameter_name="extracted_path",
            target_node_name=node3_name,
            target_parameter_name="output_dir",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node4_name,
            source_parameter_name="exec_out",
            target_node_name=node9_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node9_name,
            source_parameter_name="exec_in",
            target_node_name=node1_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node3_name,
            source_parameter_name="exec_out",
            target_node_name=node9_name,
            target_parameter_name="exec_out",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node3_name,
            source_parameter_name="output_dir",
            target_node_name=node6_name,
            target_parameter_name="path_components_ParameterListUniqueParamID_45408bf4aba54a9294b36238d61f9a2b",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node3_name,
            source_parameter_name="output_name",
            target_node_name=node6_name,
            target_parameter_name="path_components_ParameterListUniqueParamID_0023d659494d4111bef715fbbce4d573",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node6_name,
            source_parameter_name="output",
            target_node_name=node7_name,
            target_parameter_name="input_3",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="output",
            target_node_name=node5_name,
            target_parameter_name="output",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node9_name,
            source_parameter_name="exec_out",
            target_node_name=node6_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node6_name,
            source_parameter_name="exec_out",
            target_node_name=node7_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="exec_out",
            target_node_name=node5_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="url",
                node_name=node0_name,
                value=top_level_unique_values_dict["d9fd198a-766a-4115-bb62-2a22565f09bc"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="url",
                node_name=node0_name,
                value=top_level_unique_values_dict["d9fd198a-766a-4115-bb62-2a22565f09bc"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="extract_location",
                node_name=node0_name,
                value=top_level_unique_values_dict["e08615e7-4771-4f51-a45d-87cfee557417"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="extract_location",
                node_name=node0_name,
                value=top_level_unique_values_dict["e08615e7-4771-4f51-a45d-87cfee557417"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="extracted_path",
                node_name=node0_name,
                value=top_level_unique_values_dict["a5ae06cd-cfac-4ec2-9fc4-02f435497a71"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="extracted_path",
                node_name=node0_name,
                value=top_level_unique_values_dict["a5ae06cd-cfac-4ec2-9fc4-02f435497a71"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node0_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node0_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node0_name,
                value=top_level_unique_values_dict["a5ae06cd-cfac-4ec2-9fc4-02f435497a71"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node0_name,
                value=top_level_unique_values_dict["a5ae06cd-cfac-4ec2-9fc4-02f435497a71"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="request_type",
                node_name=node1_name,
                value=top_level_unique_values_dict["a162754b-2521-4706-ba45-41b0cff81738"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="request_type",
                node_name=node1_name,
                value=top_level_unique_values_dict["a162754b-2521-4706-ba45-41b0cff81738"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node1_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node1_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node1_name,
                value=top_level_unique_values_dict["849db959-99c5-4c4b-9f99-24bf48c0a492"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node1_name,
                value=top_level_unique_values_dict["849db959-99c5-4c4b-9f99-24bf48c0a492"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_category_and_key",
                node_name=node1_name,
                value=top_level_unique_values_dict["3c60b030-5c59-4de3-b738-698a9ea9ea17"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_category_and_key",
                node_name=node1_name,
                value=top_level_unique_values_dict["3c60b030-5c59-4de3-b738-698a9ea9ea17"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_success_value",
                node_name=node1_name,
                value=top_level_unique_values_dict["e08615e7-4771-4f51-a45d-87cfee557417"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_success_value",
                node_name=node1_name,
                value=top_level_unique_values_dict["e08615e7-4771-4f51-a45d-87cfee557417"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="generate_captions",
                node_name=node2_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="generate_captions",
                node_name=node2_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="agent_prompt",
                node_name=node2_name,
                value=top_level_unique_values_dict["8fe787b7-53e1-4bca-9f87-b1fa7f1216df"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="agent_prompt",
                node_name=node2_name,
                value=top_level_unique_values_dict["8fe787b7-53e1-4bca-9f87-b1fa7f1216df"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="trigger_phrase",
                node_name=node2_name,
                value=top_level_unique_values_dict["6a12e799-13b0-4078-9ca8-a63009eecd28"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="trigger_phrase",
                node_name=node2_name,
                value=top_level_unique_values_dict["6a12e799-13b0-4078-9ca8-a63009eecd28"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="image_resolution",
                node_name=node2_name,
                value=top_level_unique_values_dict["90d80844-07a6-4694-b3de-6e3c6e7d3c89"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="image_resolution",
                node_name=node2_name,
                value=top_level_unique_values_dict["90d80844-07a6-4694-b3de-6e3c6e7d3c89"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="num_repeats",
                node_name=node2_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="num_repeats",
                node_name=node2_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="dataset_folder",
                node_name=node2_name,
                value=top_level_unique_values_dict["a5ae06cd-cfac-4ec2-9fc4-02f435497a71"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="dataset_folder",
                node_name=node2_name,
                value=top_level_unique_values_dict["a5ae06cd-cfac-4ec2-9fc4-02f435497a71"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="dataset_config_path",
                node_name=node2_name,
                value=top_level_unique_values_dict["30d58adb-9b4d-4aea-a3a9-13ce909dfabf"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="dataset_config_path",
                node_name=node2_name,
                value=top_level_unique_values_dict["30d58adb-9b4d-4aea-a3a9-13ce909dfabf"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node2_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node2_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node2_name,
                value=top_level_unique_values_dict["ed84b3cc-8ae9-4682-ae84-febb81b41566"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node2_name,
                value=top_level_unique_values_dict["ed84b3cc-8ae9-4682-ae84-febb81b41566"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="exec_out",
                node_name=node3_name,
                value=top_level_unique_values_dict["fa4b5333-53bc-4239-bf30-29a9d22cedcb"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="model_family",
                node_name=node3_name,
                value=top_level_unique_values_dict["39e9da79-e6d4-4de1-81f2-23e64a3b1127"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="model_family",
                node_name=node3_name,
                value=top_level_unique_values_dict["39e9da79-e6d4-4de1-81f2-23e64a3b1127"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="flux_model",
                node_name=node3_name,
                value=top_level_unique_values_dict["f904685f-4888-4bf1-848b-ce18ba8901e7"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="flux_model",
                node_name=node3_name,
                value=top_level_unique_values_dict["f904685f-4888-4bf1-848b-ce18ba8901e7"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="dataset_config_path",
                node_name=node3_name,
                value=top_level_unique_values_dict["30d58adb-9b4d-4aea-a3a9-13ce909dfabf"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="dataset_config_path",
                node_name=node3_name,
                value=top_level_unique_values_dict["30d58adb-9b4d-4aea-a3a9-13ce909dfabf"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_dir",
                node_name=node3_name,
                value=top_level_unique_values_dict["a5ae06cd-cfac-4ec2-9fc4-02f435497a71"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_dir",
                node_name=node3_name,
                value=top_level_unique_values_dict["a5ae06cd-cfac-4ec2-9fc4-02f435497a71"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_name",
                node_name=node3_name,
                value=top_level_unique_values_dict["5f643152-9c0b-459f-ac3a-ac554cb0de6c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_name",
                node_name=node3_name,
                value=top_level_unique_values_dict["5f643152-9c0b-459f-ac3a-ac554cb0de6c"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="learning_rate",
                node_name=node3_name,
                value=top_level_unique_values_dict["9c4412ac-7a99-47e1-8998-a4a2d076728f"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="learning_rate",
                node_name=node3_name,
                value=top_level_unique_values_dict["9c4412ac-7a99-47e1-8998-a4a2d076728f"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="save_every_n_epochs",
                node_name=node3_name,
                value=top_level_unique_values_dict["6d5b7f06-00e2-4428-9a90-36b20925b79d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="save_every_n_epochs",
                node_name=node3_name,
                value=top_level_unique_values_dict["6d5b7f06-00e2-4428-9a90-36b20925b79d"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="max_train_epochs",
                node_name=node3_name,
                value=top_level_unique_values_dict["a86e110f-389b-436c-bef4-3e90136407c8"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="max_train_epochs",
                node_name=node3_name,
                value=top_level_unique_values_dict["a86e110f-389b-436c-bef4-3e90136407c8"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="network_dim",
                node_name=node3_name,
                value=top_level_unique_values_dict["c02c3580-ebdf-4727-bc09-b38f704fea8e"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="network_dim",
                node_name=node3_name,
                value=top_level_unique_values_dict["c02c3580-ebdf-4727-bc09-b38f704fea8e"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="network_alpha",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="network_alpha",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="full_bf16",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="full_bf16",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="mixed_precision",
                node_name=node3_name,
                value=top_level_unique_values_dict["c2d23049-58dc-4055-9ec0-252381272fd6"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="mixed_precision",
                node_name=node3_name,
                value=top_level_unique_values_dict["c2d23049-58dc-4055-9ec0-252381272fd6"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="save_precision",
                node_name=node3_name,
                value=top_level_unique_values_dict["c2d23049-58dc-4055-9ec0-252381272fd6"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="save_precision",
                node_name=node3_name,
                value=top_level_unique_values_dict["c2d23049-58dc-4055-9ec0-252381272fd6"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="guidance_scale",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="guidance_scale",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="fp8_base",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="fp8_base",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="highvram",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="highvram",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="max_data_loader_n_workers",
                node_name=node3_name,
                value=top_level_unique_values_dict["fb6fe015-0fd5-441d-b9b8-bf3b5eae8e98"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="max_data_loader_n_workers",
                node_name=node3_name,
                value=top_level_unique_values_dict["fb6fe015-0fd5-441d-b9b8-bf3b5eae8e98"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="randomize_seed",
                node_name=node3_name,
                value=top_level_unique_values_dict["5102ee0e-bf14-43b3-a05c-70efb5b61f02"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="randomize_seed",
                node_name=node3_name,
                value=top_level_unique_values_dict["5102ee0e-bf14-43b3-a05c-70efb5b61f02"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="seed",
                node_name=node3_name,
                value=top_level_unique_values_dict["e875f66d-a41b-49c0-870f-52ae70767cef"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="seed",
                node_name=node3_name,
                value=top_level_unique_values_dict["e875f66d-a41b-49c0-870f-52ae70767cef"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node3_name,
                value=top_level_unique_values_dict["7a7077eb-9be3-424d-9b0c-e7cdf98b0843"],
                initial_setup=True,
                is_output=True,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node3_name,
                value=top_level_unique_values_dict["00943df6-625b-4d77-baea-11352f999527"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="result_details",
                node_name=node3_name,
                value=top_level_unique_values_dict["00943df6-625b-4d77-baea-11352f999527"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node5_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node5_name,
                value=top_level_unique_values_dict["e2838058-6692-457a-ba27-4cf61fc79570"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node6_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="path_components",
                node_name=node6_name,
                value=top_level_unique_values_dict["80527f3d-e8e1-4160-833f-e7c7c1075006"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="path_components_ParameterListUniqueParamID_45408bf4aba54a9294b36238d61f9a2b",
                node_name=node6_name,
                value=top_level_unique_values_dict["3057e0e2-48f2-4175-b64d-9aa8aac730de"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="path_components_ParameterListUniqueParamID_0023d659494d4111bef715fbbce4d573",
                node_name=node6_name,
                value=top_level_unique_values_dict["5f643152-9c0b-459f-ac3a-ac554cb0de6c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node6_name,
                value=top_level_unique_values_dict["14fbd596-c47a-4947-9ae1-a53868e289e5"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node6_name,
                value=top_level_unique_values_dict["14fbd596-c47a-4947-9ae1-a53868e289e5"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node7_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_1",
                node_name=node7_name,
                value=top_level_unique_values_dict["558dbddd-d8e9-4461-926d-be96e591a374"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_2",
                node_name=node7_name,
                value=top_level_unique_values_dict["304a22a4-f82e-48c7-ae2d-c479b3ee861f"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_3",
                node_name=node7_name,
                value=top_level_unique_values_dict["14fbd596-c47a-4947-9ae1-a53868e289e5"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_4",
                node_name=node7_name,
                value=top_level_unique_values_dict["b632dcfe-a3bb-4257-9ad8-b3aac6861166"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="merge_string",
                node_name=node7_name,
                value=top_level_unique_values_dict["c9be30c8-cf08-4bd7-9ac1-e2490cbe887e"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="whitespace",
                node_name=node7_name,
                value=top_level_unique_values_dict["5102ee0e-bf14-43b3-a05c-70efb5b61f02"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node7_name,
                value=top_level_unique_values_dict["e2838058-6692-457a-ba27-4cf61fc79570"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node7_name,
                value=top_level_unique_values_dict["e2838058-6692-457a-ba27-4cf61fc79570"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node9_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node9_name,
                value=top_level_unique_values_dict["5f93cb09-ba1c-44b0-a6e5-9c4fa4a28f10"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node9_name,
                value=top_level_unique_values_dict["1ca68a1b-3589-4c97-bb1e-54c4d372bc70"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node9_name,
                value=top_level_unique_values_dict["e1180bcc-cbbf-491a-b58b-9b2287e45294"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node9_name,
                value=top_level_unique_values_dict["d500b9b0-93ba-47d3-af8c-e2e2babc904d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node9_name,
                value=top_level_unique_values_dict["d500b9b0-93ba-47d3-af8c-e2e2babc904d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_run_on_all_worker_hosts",
                node_name=node9_name,
                value=top_level_unique_values_dict["5102ee0e-bf14-43b3-a05c-70efb5b61f02"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_gpus",
                node_name=node9_name,
                value=top_level_unique_values_dict["18f615a1-764e-4426-be51-f73771f08e94"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_gpu_memory",
                node_name=node9_name,
                value=top_level_unique_values_dict["164b39cb-b634-4d93-8a56-f921467d95a0"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="exec_out",
                node_name=node9_name,
                value=top_level_unique_values_dict["fa4b5333-53bc-4239-bf30-29a9d22cedcb"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node8_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node8_name,
                value=top_level_unique_values_dict["c014e143-757c-4afd-88a6-efa2937a4c43"],
                initial_setup=True,
                is_output=False,
            )
        )


def _ensure_workflow_context():
    context_manager = GriptapeNodes.ContextManager()
    if not context_manager.has_current_flow():
        top_level_flow_request = GetTopLevelFlowRequest()
        top_level_flow_result = GriptapeNodes.handle_request(top_level_flow_request)
        if (
            isinstance(top_level_flow_result, GetTopLevelFlowResultSuccess)
            and top_level_flow_result.flow_name is not None
        ):
            flow_manager = GriptapeNodes.FlowManager()
            flow_obj = flow_manager.get_flow_by_name(top_level_flow_result.flow_name)
            context_manager.push_flow(flow_obj)


def execute_workflow(
    input: dict,
    storage_backend: str = "local",
    workflow_executor: WorkflowExecutor | None = None,
    pickle_control_flow_result: bool = False,
) -> dict | None:
    return asyncio.run(
        aexecute_workflow(
            input=input,
            storage_backend=storage_backend,
            workflow_executor=workflow_executor,
            pickle_control_flow_result=pickle_control_flow_result,
        )
    )


async def aexecute_workflow(
    input: dict,
    storage_backend: str = "local",
    workflow_executor: WorkflowExecutor | None = None,
    pickle_control_flow_result: bool = False,
) -> dict | None:
    _ensure_workflow_context()
    storage_backend_enum = StorageBackend(storage_backend)
    workflow_executor = workflow_executor or LocalWorkflowExecutor(storage_backend=storage_backend_enum)
    async with workflow_executor as executor:
        await executor.arun(flow_input=input, pickle_control_flow_result=pickle_control_flow_result)
    return executor.output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage-backend",
        choices=["local", "gtc"],
        default="local",
        help="Storage backend to use: 'local' for local filesystem or 'gtc' for Griptape Cloud",
    )
    parser.add_argument(
        "--json-input",
        default=None,
        help="JSON string containing parameter values. Takes precedence over individual parameter arguments if provided.",
    )
    parser.add_argument("--exec_out", default=None, help="Connection to the next node in the execution chain")
    args = parser.parse_args()
    flow_input = {}
    if args.json_input is not None:
        flow_input = json.loads(args.json_input)
    if args.json_input is None:
        if "Start Flow" not in flow_input:
            flow_input["Start Flow"] = {}
        if args.exec_out is not None:
            flow_input["Start Flow"]["exec_out"] = args.exec_out
    workflow_output = execute_workflow(input=flow_input, storage_backend=args.storage_backend)
    print(workflow_output)
