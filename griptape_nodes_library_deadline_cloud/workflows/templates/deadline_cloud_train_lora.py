# /// script
# dependencies = []
#
# [tool.griptape-nodes]
# name = "deadline_cloud_train_lora"
# description = "An example demonstrating how a NodeGroup can be used to send a LoRA training subflow up to AWS Deadline Cloud within a running workflow."
# schema_version = "0.14.0"
# engine_version_created_with = "0.64.1"
# node_libraries_referenced = [["Griptape Nodes Library", "0.52.2"], ["AWS Deadline Cloud Library", "0.65.1"], ["Griptape Nodes Lora Training Library", "0.61.1"]]
# node_types_used = [["Griptape Nodes Library", "EndFlow"], ["Griptape Nodes Library", "EngineNode"], ["Griptape Nodes Library", "MergeTexts"], ["Griptape Nodes Library", "Note"], ["Griptape Nodes Library", "PathJoin"], ["Griptape Nodes Library", "StandardSubflowNodeGroup"], ["Griptape Nodes Library", "StartFlow"], ["Griptape Nodes Lora Training Library", "DownloadDatasetNode"], ["Griptape Nodes Lora Training Library", "GenerateDatasetNode"], ["Griptape Nodes Lora Training Library", "TrainLoraNode"]]
# is_griptape_provided = true
# is_template = true
# creation_date = 2025-12-06T23:01:20.723077Z
# last_modified_date = 2025-12-06T23:01:20.983500Z
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
    "2b059887-0e42-4907-9341-0e2c355473a8": pickle.loads(b"\x80\x04\x89."),
    "057698e1-fdc0-49d9-b710-f47b28121a6a": pickle.loads(
        b"\x80\x04\x95\xd7\x00\x00\x00\x00\x00\x00\x00\x8c\xd3You can find your safetensor output file at: /tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_b39ejg7q/output/694d044bd3e04acdb467f5540857ffa5/dataSet_CHICKAPIGLET/my_flux_lora.safetensors\x94."
    ),
    "dbf292e3-3655-4991-8e88-cb76129d6bea": pickle.loads(
        b"\x80\x04\x95/\x00\x00\x00\x00\x00\x00\x00\x8c+You can find your safetensor output file at\x94."
    ),
    "7b6cc47f-203f-4a17-b655-6ccc97156c61": pickle.loads(
        b"\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00\x8c\x02: \x94."
    ),
    "13701e12-f5db-4244-9714-9be8410743da": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94."),
    "c018ad3f-61e5-4287-9f86-916d86ee1390": pickle.loads(
        b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x0c.safetensors\x94."
    ),
    "a28d1422-5bf0-40d9-addc-bab7ba62f043": pickle.loads(
        b"\x80\x04\x95=\x00\x00\x00\x00\x00\x00\x00\x8c9You can find your safetensor output file at: .safetensors\x94."
    ),
    "4d33a71c-38fe-40dc-8dc0-a40265261d50": pickle.loads(
        b"\x80\x04\x95\xa3\x03\x00\x00\x00\x00\x00\x00X\x9c\x03\x00\x00# Overview\n\nThis workflow runs a LoRA Training process on AWS Deadline Cloud and returns the generated safetensors file.\n\n## Libraries\n\n* Griptape Nodes Standard Library: https://github.com/griptape-ai/griptape-nodes-library-standard\n* LoRA Training Library: https://github.com/griptape-ai/griptape-nodes-lora-training-library\n  * Note: Register the Library with the `griptape-nodes-library-cuda129.json` file for compatibility with Deadline\n* AWS Deadline Cloud Library: https://github.com/griptape-ai/griptape-nodes-library-deadline-cloud\n\n## NodeGroup\n\nAll of the Nodes in the below Subflow Node Group will be packaged and submitted to AWS Deadline Cloud as a Job. This will happen when the workflow runs. The output from the Job will include a safetensors file if the LoRA training was successful. The end of this workflow will display the file path location where the safetensors file was downloaded to on your machine.\x94."
    ),
    "573ad9e3-7a2a-40f2-8d0b-8628c2a2e747": pickle.loads(
        b"\x80\x04\x95\xa4\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x8d/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10/dataSet_CHICKAPIGLET\x94\x8c\x0cmy_flux_lora\x94e."
    ),
    "ef957cb3-5a65-4d50-bf91-6a5a9a1e0366": pickle.loads(
        b"\x80\x04\x95\x91\x00\x00\x00\x00\x00\x00\x00\x8c\x8d/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10/dataSet_CHICKAPIGLET\x94."
    ),
    "d86aae8f-598f-4e0d-b3cf-8df9dec06604": pickle.loads(
        b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x0cmy_flux_lora\x94."
    ),
    "777338b0-85de-430f-acd5-a5860b6e6a2c": pickle.loads(
        b"\x80\x04\x95\x9e\x00\x00\x00\x00\x00\x00\x00\x8c\x9a/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10/dataSet_CHICKAPIGLET/my_flux_lora\x94."
    ),
    "a844b68b-4afc-4629-aceb-7b843ed30881": pickle.loads(
        b"\x80\x04\x95\x1e\x00\x00\x00\x00\x00\x00\x00\x8c\x1aAWS Deadline Cloud Library\x94."
    ),
    "9955d512-1560-4320-a0dc-3c0fedd79c1c": pickle.loads(
        b"\x80\x04\x95\x0e\x00\x00\x00\x00\x00\x00\x00\x8c\nTrain LoRA\x94."
    ),
    "dba27f27-78cc-4c91-b794-8d11dce50e93": pickle.loads(
        b'\x80\x04\x95&\x00\x00\x00\x00\x00\x00\x00\x8c"Train a LoRA on AWS Deadline Cloud\x94.'
    ),
    "8dcd8cc7-555f-43bb-82cd-46871c9a49d4": pickle.loads(b"\x80\x04]\x94."),
    "cebd8775-6aab-4749-b932-3866918663a7": pickle.loads(b"\x80\x04]\x94."),
    "c2d481de-552d-4db2-9be9-1f83900f8f3d": pickle.loads(b"\x80\x04K2."),
    "4a69b4ee-afbd-403d-8a0d-e325bca4331d": pickle.loads(
        b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05READY\x94."
    ),
    "8b00c45d-ad69-493e-bdf9-15d4881e4c22": pickle.loads(b"\x80\x04K\x00."),
    "68ea9f36-f889-4494-b791-d12b21d8096c": pickle.loads(
        b"\x80\x04\x95)\x00\x00\x00\x00\x00\x00\x00\x8c%farm-7bbde5411d444d039f12b30e007658fd\x94."
    ),
    "c43321ff-d61e-4c26-b729-05af88b0d654": pickle.loads(
        b"\x80\x04\x95*\x00\x00\x00\x00\x00\x00\x00\x8c&queue-1c93aa55070f44279d03ed7a13918099\x94."
    ),
    "d8cbcec4-cad8-4c5d-8b34-780597db4567": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bconda-forge\x94."
    ),
    "75903058-44e2-4481-985d-5e12dbfdffc9": pickle.loads(
        b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bpython=3.12\x94."
    ),
    "9c86e2ca-652b-470b-bd13-8953df010553": pickle.loads(
        b"\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x03min\x94K\x01\x8c\x03max\x94K\x02u."
    ),
    "d85d11c9-5560-4c54-84a7-5c97193b5355": pickle.loads(
        b"\x80\x04\x95K\x00\x00\x00\x00\x00\x00\x00\x8cGhttps://griptape-cloud-assets.s3.amazonaws.com/dataSet_CHICKAPIGLET.zip\x94."
    ),
    "0845d6f3-b402-474e-82c8-e266412d258c": pickle.loads(
        b"\x80\x04\x95|\x00\x00\x00\x00\x00\x00\x00\x8cx/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10\x94."
    ),
    "85e2c65a-fa8d-46a8-8397-133fc63af2b9": pickle.loads(
        b"\x80\x04\x95\x91\x00\x00\x00\x00\x00\x00\x00\x8c\x8d/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10/dataSet_CHICKAPIGLET\x94."
    ),
    "b6693a0b-0208-4359-86b9-fa12eba06136": pickle.loads(b"\x80\x04\x88."),
    "84c6a240-7b39-4c7f-88ad-adf7f822e945": pickle.loads(
        b"\x80\x04\x95\x19\x00\x00\x00\x00\x00\x00\x00\x8c\x15GetConfigValueRequest\x94."
    ),
    "799b433d-e436-4c26-aed0-a387c361989b": pickle.loads(
        b"\x80\x04\x95[\x00\x00\x00\x00\x00\x00\x00\x8cWSUCCESS: [10] Successfully returned the config value for section 'workspace_directory'.\x94."
    ),
    "23de47ee-bf59-401c-b845-debc48e3d8b0": pickle.loads(
        b"\x80\x04\x95\x17\x00\x00\x00\x00\x00\x00\x00\x8c\x13workspace_directory\x94."
    ),
    "2d99985c-216b-45a1-a4bd-48a0048d16cf": pickle.loads(b"\x80\x04]\x94."),
    "21470592-e490-471d-bc9c-3343606fd533": pickle.loads(
        b"\x80\x04\x95s\x00\x00\x00\x00\x00\x00\x00\x8coDescribe this image with descriptive tags. Include details about the subject, setting, colors, mood, and style.\x94."
    ),
    "658fdb8b-e9e2-47e2-bfd1-60cfd10635d7": pickle.loads(b"\x80\x04]\x94."),
    "429ca43f-47df-4355-a67c-a7be67431ff4": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07cartoon\x94."
    ),
    "74daae1e-588b-4fab-921d-d7bfb28375d5": pickle.loads(b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\x00\x02."),
    "b0e8a099-e200-4842-99a2-a43f9748e91e": pickle.loads(
        b"\x80\x04\x95\x9e\x00\x00\x00\x00\x00\x00\x00\x8c\x9a/tmp/NodeGroup_AWS_Deadline_Cloud_Library_packaged_flow_deadline_bundle_l00kpxc6/output/4a193e3b099f4b5ba070389f6fa2ac10/dataSet_CHICKAPIGLET/dataset.toml\x94."
    ),
    "3fad87b1-6dae-4912-b734-aacc45f0aae9": pickle.loads(
        b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07Success\x94."
    ),
    "7babcceb-d0c9-4ae9-891e-e35a04a187f4": pickle.loads(
        b"\x80\x04\x95\x1b\x00\x00\x00\x00\x00\x00\x00\x8c\x17Control Input Selection\x94."
    ),
    "4f4713c3-c278-4f18-b782-e19aa47b5f44": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06FLUX.1\x94."
    ),
    "94478748-67eb-441d-96a7-d6aa6da329b1": pickle.loads(
        b"\x80\x04\x95 \x00\x00\x00\x00\x00\x00\x00\x8c\x1cblack-forest-labs/FLUX.1-dev\x94."
    ),
    "d591c86e-6b7f-46aa-8cd1-685a2ae5e46b": pickle.loads(
        b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x0cmy_flux_lora\x94."
    ),
    "0a29c8a6-8dcb-42e8-b001-c9c2970104e3": pickle.loads(
        b"\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00G?J6\xe2\xeb\x1cC-."
    ),
    "71f61fca-c22f-4d44-ba42-da5e7b861db0": pickle.loads(b"\x80\x04K\x08."),
    "64b020b4-fc3b-4449-af47-8f1fcc598197": pickle.loads(b"\x80\x04K\x10."),
    "b0e4c550-62ea-405d-ac34-f45cc08963ae": pickle.loads(b"\x80\x04K\x04."),
    "25fc0399-29fe-450d-b8db-0c9263bbc391": pickle.loads(
        b"\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04bf16\x94."
    ),
    "f1ffa38d-de80-441e-a033-b85a96f36637": pickle.loads(b"\x80\x04K\x02."),
    "6f161b64-d8ad-4821-84c3-5561bfc846b5": pickle.loads(b"\x80\x04\x89."),
    "7682f43c-486a-4bc7-bf44-0c30a3fba42c": pickle.loads(b"\x80\x04K*."),
    "28b91949-5e3c-409a-9405-097cddafca54": pickle.loads(
        b"\x80\x04\x951\x00\x00\x00\x00\x00\x00\x00\x8c-SUCCESS: LoRA training executed successfully.\x94."
    ),
}

"# Create the Flow, then do work within it as context."

flow0_name = GriptapeNodes.handle_request(
    CreateFlowRequest(parent_flow_name=None, flow_name="ControlFlow_1", set_as_new_context=False, metadata={})
).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="StartFlow",
            specific_library_name="Griptape Nodes Library",
            node_name="Start Flow",
            metadata={
                "position": {"x": -1188.4680657484485, "y": -1758.09940346112},
                "tempId": "placing-1764036813381-cun22",
                "library_node_metadata": NodeMetadata(
                    category="workflows",
                    description="Define the start of a workflow and pass parameters into the flow",
                    display_name="Start Flow",
                    tags=None,
                    icon=None,
                    color=None,
                    group="create",
                    deprecation=None,
                    is_node_group=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "StartFlow",
                "showaddparameter": True,
                "size": {"width": 940, "height": 1386},
                "category": "workflows",
            },
            resolution="resolved",
            initial_setup=True,
        )
    ).node_name
    node1_name = GriptapeNodes.handle_request(
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
                    is_node_group=None,
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
    with GriptapeNodes.ContextManager().node(node1_name):
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
    node2_name = GriptapeNodes.handle_request(
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
                    is_node_group=None,
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
    node3_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="Note",
            specific_library_name="Griptape Nodes Library",
            node_name="Note",
            metadata={
                "position": {"x": 47.63740729474671, "y": -2564.9737855651842},
                "tempId": "placing-1764204840994-phevm",
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
                "size": {"width": 1319, "height": 754},
                "category": "misc",
            },
            initial_setup=True,
        )
    ).node_name
    node4_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="PathJoin",
            specific_library_name="Griptape Nodes Library",
            node_name="Path Join",
            metadata={
                "position": {"x": 5276.137153270917, "y": -1683.7637498379243},
                "tempId": "placing-1764633161226-yyp6mk",
                "library_node_metadata": NodeMetadata(
                    category="files",
                    description="Join multiple path components together to create a file path using appropriate path separators",
                    display_name="Path Join",
                    tags=None,
                    icon="Combine",
                    color=None,
                    group=None,
                    deprecation=None,
                    is_node_group=None,
                ),
                "library": "Griptape Nodes Library",
                "node_type": "PathJoin",
                "showaddparameter": False,
                "size": {"width": 925, "height": 1146},
                "category": "files",
            },
            initial_setup=True,
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            AddParameterToNodeRequest(
                parameter_name="path_components_ParameterListUniqueParamID_03709160c98a4807a92babdc6f5b29bf",
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
                parameter_name="path_components_ParameterListUniqueParamID_3437e7970efe4a9995843409068d3b4c",
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
        node5_name = GriptapeNodes.handle_request(
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
                        is_node_group=None,
                    ),
                    "library": "Griptape Nodes Lora Training Library",
                    "node_type": "DownloadDatasetNode",
                    "position": {"x": 1328.9081261812635, "y": 323.1440650926111},
                    "size": {"width": 902, "height": 884},
                    "showaddparameter": False,
                },
                initial_setup=True,
            )
        ).node_name
        node6_name = GriptapeNodes.handle_request(
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
                        is_node_group=None,
                    ),
                    "library": "Griptape Nodes Library",
                    "node_type": "EngineNode",
                    "position": {"x": 298, "y": 323.1440650926111},
                    "size": {"width": 801, "height": 897},
                    "showaddparameter": False,
                    "category": "engine",
                },
                initial_setup=True,
            )
        ).node_name
        with GriptapeNodes.ContextManager().node(node6_name):
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
                    parameter_name="input_failure_log_level",
                    tooltip="Input for failure_log_level (type: int)",
                    type="int",
                    input_types=["int"],
                    output_type="int",
                    ui_options={"display_name": "failure_log_level (optional)"},
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
        node7_name = GriptapeNodes.handle_request(
            CreateNodeRequest(
                node_type="GenerateDatasetNode",
                specific_library_name="Griptape Nodes Lora Training Library",
                node_name="Generate Lora Dataset",
                metadata={
                    "position": {"x": 2369.808914939722, "y": 323.1440650926111},
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
                        is_node_group=None,
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
        with GriptapeNodes.ContextManager().node(node7_name):
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
        node8_name = GriptapeNodes.handle_request(
            CreateNodeRequest(
                node_type="TrainLoraNode",
                specific_library_name="Griptape Nodes Lora Training Library",
                node_name="Train Lora",
                metadata={
                    "position": {"x": 3395.905461692726, "y": 246},
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
                        is_node_group=None,
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
        GriptapeNodes.handle_request(
            CreateConnectionRequest(
                source_node_name=node5_name,
                source_parameter_name="extracted_path",
                target_node_name=node7_name,
                target_parameter_name="dataset_folder",
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            CreateConnectionRequest(
                source_node_name=node7_name,
                source_parameter_name="dataset_config_path",
                target_node_name=node8_name,
                target_parameter_name="dataset_config_path",
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            CreateConnectionRequest(
                source_node_name=node6_name,
                source_parameter_name="output_success_value",
                target_node_name=node5_name,
                target_parameter_name="extract_location",
                initial_setup=True,
            )
        )
        GriptapeNodes.handle_request(
            CreateConnectionRequest(
                source_node_name=node5_name,
                source_parameter_name="extracted_path",
                target_node_name=node8_name,
                target_parameter_name="output_dir",
                initial_setup=True,
            )
        )
        with GriptapeNodes.ContextManager().node(node5_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="url",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["d85d11c9-5560-4c54-84a7-5c97193b5355"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="url",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["d85d11c9-5560-4c54-84a7-5c97193b5355"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="extract_location",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["0845d6f3-b402-474e-82c8-e266412d258c"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="extract_location",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["0845d6f3-b402-474e-82c8-e266412d258c"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="extracted_path",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["85e2c65a-fa8d-46a8-8397-133fc63af2b9"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="extracted_path",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["85e2c65a-fa8d-46a8-8397-133fc63af2b9"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="result_details",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["85e2c65a-fa8d-46a8-8397-133fc63af2b9"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="result_details",
                    node_name=node5_name,
                    value=top_level_unique_values_dict["85e2c65a-fa8d-46a8-8397-133fc63af2b9"],
                    initial_setup=True,
                    is_output=True,
                )
            )
        with GriptapeNodes.ContextManager().node(node6_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="request_type",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["84c6a240-7b39-4c7f-88ad-adf7f822e945"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="request_type",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["84c6a240-7b39-4c7f-88ad-adf7f822e945"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="result_details",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["799b433d-e436-4c26-aed0-a387c361989b"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="result_details",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["799b433d-e436-4c26-aed0-a387c361989b"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="input_category_and_key",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["23de47ee-bf59-401c-b845-debc48e3d8b0"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="input_category_and_key",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["23de47ee-bf59-401c-b845-debc48e3d8b0"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output_success_value",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["0845d6f3-b402-474e-82c8-e266412d258c"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output_success_value",
                    node_name=node6_name,
                    value=top_level_unique_values_dict["0845d6f3-b402-474e-82c8-e266412d258c"],
                    initial_setup=True,
                    is_output=True,
                )
            )
        with GriptapeNodes.ContextManager().node(node7_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="images",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["2d99985c-216b-45a1-a4bd-48a0048d16cf"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="generate_captions",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="generate_captions",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="agent_prompt",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["21470592-e490-471d-bc9c-3343606fd533"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="agent_prompt",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["21470592-e490-471d-bc9c-3343606fd533"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="captions",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["658fdb8b-e9e2-47e2-bfd1-60cfd10635d7"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="trigger_phrase",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["429ca43f-47df-4355-a67c-a7be67431ff4"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="trigger_phrase",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["429ca43f-47df-4355-a67c-a7be67431ff4"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="image_resolution",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["74daae1e-588b-4fab-921d-d7bfb28375d5"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="image_resolution",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["74daae1e-588b-4fab-921d-d7bfb28375d5"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="num_repeats",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="num_repeats",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="dataset_folder",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["85e2c65a-fa8d-46a8-8397-133fc63af2b9"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="dataset_folder",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["85e2c65a-fa8d-46a8-8397-133fc63af2b9"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="dataset_config_path",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["b0e8a099-e200-4842-99a2-a43f9748e91e"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="dataset_config_path",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["b0e8a099-e200-4842-99a2-a43f9748e91e"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="result_details",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["3fad87b1-6dae-4912-b734-aacc45f0aae9"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="result_details",
                    node_name=node7_name,
                    value=top_level_unique_values_dict["3fad87b1-6dae-4912-b734-aacc45f0aae9"],
                    initial_setup=True,
                    is_output=True,
                )
            )
        with GriptapeNodes.ContextManager().node(node8_name):
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="exec_out",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["7babcceb-d0c9-4ae9-891e-e35a04a187f4"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="model_family",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["4f4713c3-c278-4f18-b782-e19aa47b5f44"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="model_family",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["4f4713c3-c278-4f18-b782-e19aa47b5f44"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="flux_model",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["94478748-67eb-441d-96a7-d6aa6da329b1"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="flux_model",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["94478748-67eb-441d-96a7-d6aa6da329b1"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="dataset_config_path",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b0e8a099-e200-4842-99a2-a43f9748e91e"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="dataset_config_path",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b0e8a099-e200-4842-99a2-a43f9748e91e"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output_dir",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["85e2c65a-fa8d-46a8-8397-133fc63af2b9"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output_dir",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["85e2c65a-fa8d-46a8-8397-133fc63af2b9"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output_name",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["d591c86e-6b7f-46aa-8cd1-685a2ae5e46b"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="output_name",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["d591c86e-6b7f-46aa-8cd1-685a2ae5e46b"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="learning_rate",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["0a29c8a6-8dcb-42e8-b001-c9c2970104e3"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="learning_rate",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["0a29c8a6-8dcb-42e8-b001-c9c2970104e3"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="save_every_n_epochs",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["71f61fca-c22f-4d44-ba42-da5e7b861db0"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="save_every_n_epochs",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["71f61fca-c22f-4d44-ba42-da5e7b861db0"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="max_train_epochs",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["64b020b4-fc3b-4449-af47-8f1fcc598197"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="max_train_epochs",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["64b020b4-fc3b-4449-af47-8f1fcc598197"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="network_dim",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b0e4c550-62ea-405d-ac34-f45cc08963ae"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="network_dim",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b0e4c550-62ea-405d-ac34-f45cc08963ae"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="network_alpha",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="network_alpha",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="full_bf16",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="full_bf16",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="mixed_precision",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["25fc0399-29fe-450d-b8db-0c9263bbc391"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="mixed_precision",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["25fc0399-29fe-450d-b8db-0c9263bbc391"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="save_precision",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["25fc0399-29fe-450d-b8db-0c9263bbc391"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="save_precision",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["25fc0399-29fe-450d-b8db-0c9263bbc391"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="guidance_scale",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="guidance_scale",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="fp8_base",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="fp8_base",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="highvram",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="highvram",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="max_data_loader_n_workers",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["f1ffa38d-de80-441e-a033-b85a96f36637"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="max_data_loader_n_workers",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["f1ffa38d-de80-441e-a033-b85a96f36637"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="randomize_seed",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["6f161b64-d8ad-4821-84c3-5561bfc846b5"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="randomize_seed",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["6f161b64-d8ad-4821-84c3-5561bfc846b5"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="seed",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["7682f43c-486a-4bc7-bf44-0c30a3fba42c"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="seed",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["7682f43c-486a-4bc7-bf44-0c30a3fba42c"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="was_successful",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["b6693a0b-0208-4359-86b9-fa12eba06136"],
                    initial_setup=True,
                    is_output=True,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="result_details",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["28b91949-5e3c-409a-9405-097cddafca54"],
                    initial_setup=True,
                    is_output=False,
                )
            )
            GriptapeNodes.handle_request(
                SetParameterValueRequest(
                    parameter_name="result_details",
                    node_name=node8_name,
                    value=top_level_unique_values_dict["28b91949-5e3c-409a-9405-097cddafca54"],
                    initial_setup=True,
                    is_output=True,
                )
            )
    node9_name = GriptapeNodes.handle_request(
        CreateNodeRequest(
            node_type="StandardSubflowNodeGroup",
            specific_library_name="Griptape Nodes Library",
            node_name="Subflow Node Group",
            metadata={
                "position": {"x": 47.63740729474671, "y": -1744.7637498379243},
                "size": {"width": 4747, "height": 1368},
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
                "expanded_dimensions": {"width": 4747, "height": 1368},
                "right_parameters": ["exec_out", "output_dir", "output_name"],
                "left_parameters": ["exec_in"],
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
            node_names_to_add=[node5_name, node6_name, node7_name, node8_name],
        )
    ).node_name
    with GriptapeNodes.ContextManager().node(node9_name):
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
                parameter_name="output_dir",
                tooltip="Enter text/string for output_dir.",
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
                parameter_name="output_name",
                tooltip="Enter text/string for output_name.",
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
        CreateConnectionRequest(
            source_node_name=node2_name,
            source_parameter_name="output",
            target_node_name=node1_name,
            target_parameter_name="output",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node2_name,
            source_parameter_name="exec_out",
            target_node_name=node1_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node4_name,
            source_parameter_name="exec_out",
            target_node_name=node2_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node4_name,
            source_parameter_name="output",
            target_node_name=node2_name,
            target_parameter_name="input_3",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="exec_out",
            target_node_name=node9_name,
            target_parameter_name="exec_out",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node9_name,
            source_parameter_name="exec_out",
            target_node_name=node4_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="output_dir",
            target_node_name=node9_name,
            target_parameter_name="output_dir",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node9_name,
            source_parameter_name="output_dir",
            target_node_name=node4_name,
            target_parameter_name="path_components_ParameterListUniqueParamID_03709160c98a4807a92babdc6f5b29bf",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node8_name,
            source_parameter_name="output_name",
            target_node_name=node9_name,
            target_parameter_name="output_name",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node9_name,
            source_parameter_name="output_name",
            target_node_name=node4_name,
            target_parameter_name="path_components_ParameterListUniqueParamID_3437e7970efe4a9995843409068d3b4c",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node0_name,
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
            target_node_name=node6_name,
            target_parameter_name="exec_in",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="extracted_path",
            target_node_name=node7_name,
            target_parameter_name="dataset_folder",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="dataset_config_path",
            target_node_name=node8_name,
            target_parameter_name="dataset_config_path",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node6_name,
            source_parameter_name="output_success_value",
            target_node_name=node5_name,
            target_parameter_name="extract_location",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="extracted_path",
            target_node_name=node8_name,
            target_parameter_name="output_dir",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="extracted_path",
            target_node_name=node7_name,
            target_parameter_name="dataset_folder",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node7_name,
            source_parameter_name="dataset_config_path",
            target_node_name=node8_name,
            target_parameter_name="dataset_config_path",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node6_name,
            source_parameter_name="output_success_value",
            target_node_name=node5_name,
            target_parameter_name="extract_location",
            initial_setup=True,
        )
    )
    GriptapeNodes.handle_request(
        CreateConnectionRequest(
            source_node_name=node5_name,
            source_parameter_name="extracted_path",
            target_node_name=node8_name,
            target_parameter_name="output_dir",
            initial_setup=True,
        )
    )
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="was_successful",
                node_name=node1_name,
                value=top_level_unique_values_dict["2b059887-0e42-4907-9341-0e2c355473a8"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node1_name,
                value=top_level_unique_values_dict["057698e1-fdc0-49d9-b710-f47b28121a6a"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_1",
                node_name=node2_name,
                value=top_level_unique_values_dict["dbf292e3-3655-4991-8e88-cb76129d6bea"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_2",
                node_name=node2_name,
                value=top_level_unique_values_dict["7b6cc47f-203f-4a17-b655-6ccc97156c61"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_3",
                node_name=node2_name,
                value=top_level_unique_values_dict["13701e12-f5db-4244-9714-9be8410743da"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="input_4",
                node_name=node2_name,
                value=top_level_unique_values_dict["c018ad3f-61e5-4287-9f86-916d86ee1390"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="merge_string",
                node_name=node2_name,
                value=top_level_unique_values_dict["13701e12-f5db-4244-9714-9be8410743da"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="whitespace",
                node_name=node2_name,
                value=top_level_unique_values_dict["2b059887-0e42-4907-9341-0e2c355473a8"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node2_name,
                value=top_level_unique_values_dict["a28d1422-5bf0-40d9-addc-bab7ba62f043"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node2_name,
                value=top_level_unique_values_dict["a28d1422-5bf0-40d9-addc-bab7ba62f043"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node3_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="note",
                node_name=node3_name,
                value=top_level_unique_values_dict["4d33a71c-38fe-40dc-8dc0-a40265261d50"],
                initial_setup=True,
                is_output=False,
            )
        )
    with GriptapeNodes.ContextManager().node(node4_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="path_components",
                node_name=node4_name,
                value=top_level_unique_values_dict["573ad9e3-7a2a-40f2-8d0b-8628c2a2e747"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="path_components_ParameterListUniqueParamID_03709160c98a4807a92babdc6f5b29bf",
                node_name=node4_name,
                value=top_level_unique_values_dict["ef957cb3-5a65-4d50-bf91-6a5a9a1e0366"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="path_components_ParameterListUniqueParamID_3437e7970efe4a9995843409068d3b4c",
                node_name=node4_name,
                value=top_level_unique_values_dict["d86aae8f-598f-4e0d-b3cf-8df9dec06604"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node4_name,
                value=top_level_unique_values_dict["777338b0-85de-430f-acd5-a5860b6e6a2c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output",
                node_name=node4_name,
                value=top_level_unique_values_dict["777338b0-85de-430f-acd5-a5860b6e6a2c"],
                initial_setup=True,
                is_output=True,
            )
        )
    with GriptapeNodes.ContextManager().node(node9_name):
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="execution_environment",
                node_name=node9_name,
                value=top_level_unique_values_dict["a844b68b-4afc-4629-aceb-7b843ed30881"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_name",
                node_name=node9_name,
                value=top_level_unique_values_dict["9955d512-1560-4320-a0dc-3c0fedd79c1c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_job_description",
                node_name=node9_name,
                value=top_level_unique_values_dict["dba27f27-78cc-4c91-b794-8d11dce50e93"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_input_paths",
                node_name=node9_name,
                value=top_level_unique_values_dict["8dcd8cc7-555f-43bb-82cd-46871c9a49d4"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_attachment_output_paths",
                node_name=node9_name,
                value=top_level_unique_values_dict["cebd8775-6aab-4749-b932-3866918663a7"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_priority",
                node_name=node9_name,
                value=top_level_unique_values_dict["c2d481de-552d-4db2-9be9-1f83900f8f3d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_initial_state",
                node_name=node9_name,
                value=top_level_unique_values_dict["4a69b4ee-afbd-403d-8a0d-e325bca4331d"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_failed_tasks",
                node_name=node9_name,
                value=top_level_unique_values_dict["8b00c45d-ad69-493e-bdf9-15d4881e4c22"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_max_task_retries",
                node_name=node9_name,
                value=top_level_unique_values_dict["8b00c45d-ad69-493e-bdf9-15d4881e4c22"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_farm_id",
                node_name=node9_name,
                value=top_level_unique_values_dict["68ea9f36-f889-4494-b791-d12b21d8096c"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_queue_id",
                node_name=node9_name,
                value=top_level_unique_values_dict["c43321ff-d61e-4c26-b729-05af88b0d654"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_storage_profile_id",
                node_name=node9_name,
                value=top_level_unique_values_dict["13701e12-f5db-4244-9714-9be8410743da"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_channels",
                node_name=node9_name,
                value=top_level_unique_values_dict["d8cbcec4-cad8-4c5d-8b34-780597db4567"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_conda_packages",
                node_name=node9_name,
                value=top_level_unique_values_dict["75903058-44e2-4481-985d-5e12dbfdffc9"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_run_on_all_worker_hosts",
                node_name=node9_name,
                value=top_level_unique_values_dict["2b059887-0e42-4907-9341-0e2c355473a8"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="deadlinecloudstartflow_gpus",
                node_name=node9_name,
                value=top_level_unique_values_dict["9c86e2ca-652b-470b-bd13-8953df010553"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="griptapecloudstartflow_enable_webhook_integration",
                node_name=node9_name,
                value=top_level_unique_values_dict["2b059887-0e42-4907-9341-0e2c355473a8"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_dir",
                node_name=node9_name,
                value=top_level_unique_values_dict["ef957cb3-5a65-4d50-bf91-6a5a9a1e0366"],
                initial_setup=True,
                is_output=False,
            )
        )
        GriptapeNodes.handle_request(
            SetParameterValueRequest(
                parameter_name="output_name",
                node_name=node9_name,
                value=top_level_unique_values_dict["d86aae8f-598f-4e0d-b3cf-8df9dec06604"],
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
