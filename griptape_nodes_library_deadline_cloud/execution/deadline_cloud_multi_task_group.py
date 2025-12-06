from __future__ import annotations

import logging
from typing import Any, TypeVar

from griptape_nodes.common.node_executor import PublishWorkflowStartEndNodes
from griptape_nodes.exe_types.core_types import (
    Parameter,
    ParameterMode,
    ParameterTypeBuiltin,
)
from griptape_nodes.exe_types.node_groups.base_node_group import BaseNodeGroup
from griptape_nodes.exe_types.node_groups.subflow_node_group import SubflowNodeGroup
from griptape_nodes.exe_types.node_types import (
    LOCAL_EXECUTION,
    Connection,
)
from griptape_nodes.retained_mode.events.connection_events import (
    DeleteConnectionRequest,
)
from griptape_nodes.retained_mode.events.flow_events import (
    PackageNodesAsSerializedFlowRequest,
    PackageNodesAsSerializedFlowResultSuccess,
)
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes
from griptape_nodes.traits.options import Options
from publish import LIBRARY_NAME
from publish.deadline_cloud_end_flow import DeadlineCloudEndFlow
from publish.deadline_cloud_start_flow import DeadlineCloudStartFlow

logger = logging.getLogger("griptape_nodes")

T = TypeVar("T")


class DeadlineCloudMultiTaskGroup(SubflowNodeGroup, BaseNodeGroup):
    """A SubflowNodeGroup that represents a Deadline Job defined with multiple Tasks.

    This SubflowNodeGroup is designed to encapsulate multiple tasks that are part of a single Job
    submitted to the AWS Deadline Cloud render farm management system.

    The subflow defined by the Nodes within this Group is the unit of work that will be performed by each task.
    The input for each invocation of the Group will be provided as a list of inputs on the Group itself, one for each task.

    Attributes:
        name (str): The name of the node group.
        description (str): A brief description of the node group's purpose.
    """

    def __init__(
        self,
        name: str,
        metadata: dict[Any, Any] | None = None,
    ) -> None:
        BaseNodeGroup.__init__(self, name=name, metadata=metadata)

        # Metadata overrides
        self.metadata["color"] = "#00c951"
        self.metadata["hideaddparameter"] = True

        self.execution_environment = Parameter(
            name="execution_environment",
            tooltip="Environment that the group should execute in",
            type=ParameterTypeBuiltin.STR,
            allowed_modes={ParameterMode.PROPERTY},
            default_value=LIBRARY_NAME,
            traits={Options(choices=[LIBRARY_NAME, LOCAL_EXECUTION])},
        )
        self.add_parameter(self.execution_environment)
        # Track mapping from proxy parameter name to (original_node, original_param_name)
        self._proxy_param_to_connections = {}
        if "execution_environment" not in self.metadata:
            self.metadata["execution_environment"] = {}
        self.metadata["execution_environment"]["Griptape Nodes Library"] = {
            "start_flow_node": "StartFlow",
            "parameter_names": {},
        }

        # Add parameters from registered StartFlow nodes for each publishing library
        self._add_start_flow_parameters()

        # Iteration parameters
        self.items_list = Parameter(
            name="items",
            tooltip="List or dictionary to iterate through",
            input_types=["list", "dict"],
            allowed_modes={ParameterMode.INPUT},
        )
        self.add_parameter(self.items_list)
        self.current_item = Parameter(
            name="current_item",
            tooltip="Current item being processed",
            output_type=ParameterTypeBuiltin.ALL.value,
            allowed_modes={ParameterMode.OUTPUT},
            settable=False,
        )
        self.add_parameter(self.current_item)
        self.metadata["left_parameters"] = ["items", "current_item"]

        self.new_item_to_add = Parameter(
            name="new_item_to_add",
            tooltip="Item to add to results list",
            type=ParameterTypeBuiltin.ANY.value,
            allowed_modes={ParameterMode.INPUT},
        )
        self.add_parameter(self.new_item_to_add)
        self.results = Parameter(
            name="results",
            tooltip="Collected loop results",
            output_type="list",
            allowed_modes={ParameterMode.OUTPUT},
        )
        self.add_parameter(self.results)
        self.metadata["right_parameters"] = ["new_item_to_add", "results"]

    def _add_start_flow_parameters(self) -> None:
        """Add parameters from ONLY the DeadlineCloudStartFlow nodes to this SubflowNodeGroup.

        For the AWS Deadline Cloud Library that has registered a PublishWorkflowRequest handler with
        a StartFlow node, this method:
        1. Creates a temporary instance of that StartFlow node
        2. Extracts all its parameters
        3. Adds them to this SubflowNodeGroup with a prefix based on the class name
        4. Stores metadata mapping execution environments to their parameters
        """
        from griptape_nodes.retained_mode.events.workflow_events import PublishWorkflowRequest
        from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

        # Initialize metadata structure for execution environment mappings
        if self.metadata is None:
            self.metadata = {}
        if "execution_environment" not in self.metadata:
            self.metadata["execution_environment"] = {}

        # Get all libraries that have registered PublishWorkflowRequest handlers
        library_manager = GriptapeNodes.LibraryManager()
        event_handlers = library_manager.get_registered_event_handlers(PublishWorkflowRequest)

        if LIBRARY_NAME not in event_handlers:
            msg = f"No PublishWorkflowRequest handler registered for library '{LIBRARY_NAME}'."
            raise ValueError(msg)

        self._process_library_start_flow_parameters(LIBRARY_NAME, event_handlers[LIBRARY_NAME])

    def map_external_connection(self, conn: Connection, *, is_incoming: bool) -> bool:  # noqa: ARG002
        """Track a connection to/from a node in the group and rewire it through a proxy parameter.

        Args:
            conn: The external connection to track
            conn_id: ID of the connection
            is_incoming: True if connection is coming INTO the group
        """
        # No external connections permitted for this Group

        request = DeleteConnectionRequest(
            conn.source_parameter.name,
            conn.target_parameter.name,
            conn.source_node.name,
            conn.target_node.name,
        )
        GriptapeNodes.handle_request(request)
        return False

    def validate_before_workflow_run(self) -> list[Exception] | None:
        exceptions: list[Exception] = []
        exceptions.extend(super().validate_before_workflow_run() or [])

        # Set this to enable the Node to handle aprocess, rather than the core engine handling the Library publish
        try:
            self.set_parameter_value("execution_environment", LOCAL_EXECUTION)
        except Exception as e:
            exceptions.append(e)
        return exceptions if exceptions else None

    # Execution

    def _get_iteration_items(self) -> list[Any]:
        """Get the list of items to iterate over.

        Accepts either a list or dict. If dict, converts to list of {"key": k, "value": v} dicts.
        """
        items = self.get_parameter_value("items")

        # Handle case where items parameter is not connected or has no value
        if items is None:
            logger.info("ForEach Start '%s': No items provided, skipping loop execution", self.name)
            return []

        # Handle dict input - convert to list of {"key": k, "value": v} dicts
        if isinstance(items, dict):
            if len(items) == 0:
                logger.info("ForEach Start '%s': Empty dictionary provided, skipping loop execution", self.name)
                return []
            return [{"key": k, "value": v} for k, v in items.items()]

        # Handle list input
        if isinstance(items, list):
            if len(items) == 0:
                logger.info("ForEach Start '%s': Empty list provided, skipping loop execution", self.name)
            return items

        # Invalid type
        error_msg = (
            f"{self.__class__.__name__} '{self.name}' expected a list or dict but got {type(items).__name__}: {items}"
        )
        raise TypeError(error_msg)

    def _initialize_iteration_data(self) -> None:
        """Initialize iteration-specific data and state."""
        # Get the items list for ForEach
        self._items = self._get_iteration_items()

    def _get_total_iterations(self) -> int:
        """Return the total number of iterations for this loop."""
        return len(self._items) if self._items else 0

    async def _package_group_body(
        self,
    ) -> PackageNodesAsSerializedFlowResultSuccess | None:
        """Package and publish a workflow for subprocess execution.

        Returns:
            PublishLocalWorkflowResult containing workflow_result, file_name, and output_parameter_prefix
        """
        sanitized_node_name = self.name.replace(" ", "_")
        output_parameter_prefix = f"{sanitized_node_name}_packaged_node_"
        workflow_start_end_nodes = PublishWorkflowStartEndNodes(
            start_flow_node_type=DeadlineCloudStartFlow.__name__,
            start_flow_node_library_name=LIBRARY_NAME,
            end_flow_node_type=DeadlineCloudEndFlow.__name__,
            end_flow_node_library_name=LIBRARY_NAME,
        )

        node_names = list(self.get_all_nodes().keys())

        if len(node_names) == 0:
            return None

        request = PackageNodesAsSerializedFlowRequest(
            node_names=node_names,
            start_node_type=workflow_start_end_nodes.start_flow_node_type,
            end_node_type=workflow_start_end_nodes.end_flow_node_type,
            start_node_library_name=workflow_start_end_nodes.start_flow_node_library_name,
            end_node_library_name=workflow_start_end_nodes.end_flow_node_library_name,
            output_parameter_prefix=output_parameter_prefix,
            entry_control_node_name=None,
            entry_control_parameter_name=None,
            node_group_name=self.name,
        )
        package_result = GriptapeNodes.handle_request(request)
        if not isinstance(package_result, PackageNodesAsSerializedFlowResultSuccess):
            msg = f"Failed to package node '{self.name}'. Error: {package_result.result_details}"
            raise RuntimeError(msg)  # noqa: TRY004

        return package_result

    def _get_parameter_values_per_iteration(  # noqa: C901
        self,
        package_result: PackageNodesAsSerializedFlowResultSuccess,
    ) -> dict[int, dict[str, Any]]:
        """Get parameter values for each iteration based on the items list.

        This maps iteration index to parameter values that should be set on the packaged flow's StartFlow node.
        For DeadlineCloudMultiTaskGroup, this maps the current_item output to the appropriate StartFlow parameter.

        Args:
            package_result: PackageNodesAsSerializedFlowResultSuccess containing parameter_name_mappings

        Returns:
            Dict mapping iteration_index -> {startflow_param_name: value}
        """
        from griptape_nodes.retained_mode.events.connection_events import (
            ListConnectionsForNodeRequest,
            ListConnectionsForNodeResultSuccess,
        )

        total_iterations = self._get_total_iterations()

        # Get the items for each iteration
        current_item_values = list(self._items) if self._items else []

        # Get outgoing connections from this node's current_item parameter
        list_connections_request = ListConnectionsForNodeRequest(node_name=self.name)
        list_connections_result = GriptapeNodes.handle_request(list_connections_request)
        if not isinstance(list_connections_result, ListConnectionsForNodeResultSuccess):
            msg = f"Failed to list connections for node {self.name}: {list_connections_result.result_details}"
            raise RuntimeError(msg)  # noqa: TRY004

        outgoing_connections = list_connections_result.outgoing_connections

        # Get Start node's parameter mappings (index 0 in the list)
        # The start_node_param_mappings tells us: startflow_param_name -> OriginalNodeParameter(target_node, target_param)
        start_node_mapping = package_result.parameter_name_mappings[0]
        start_node_param_mappings = start_node_mapping.parameter_mappings

        parameter_val_mappings: dict[int, dict[str, Any]] = {}
        for iteration_index in range(total_iterations):
            iteration_values: dict[str, Any] = {}

            # For each outgoing data connection from this node's current_item
            for conn in outgoing_connections:
                source_param_name = conn.source_parameter_name
                target_node_name = conn.target_node_name
                target_param_name = conn.target_parameter_name

                # Only care about connections from current_item
                if source_param_name != "current_item":
                    continue

                # If target is a SubflowNodeGroup (this node), follow the internal connection
                node_manager = GriptapeNodes.NodeManager()
                flow_manager = GriptapeNodes.FlowManager()
                try:
                    target_node = node_manager.get_node_by_name(target_node_name)
                except ValueError:
                    msg = f"Failed to get node {target_node_name} for connection from {self.name}."
                    logger.error(msg)
                    continue

                if isinstance(target_node, SubflowNodeGroup):
                    # Get connections from this proxy parameter to find the actual internal target
                    connections = flow_manager.get_connections()
                    proxy_param = target_node.get_parameter_by_name(target_param_name)
                    if proxy_param:
                        internal_connections = connections.get_all_outgoing_connections(target_node)
                        for internal_conn in internal_connections:
                            if (
                                internal_conn.source_parameter.name == target_param_name
                                and internal_conn.is_node_group_internal
                            ):
                                target_node_name = internal_conn.target_node.name
                                target_param_name = internal_conn.target_parameter.name
                                break

                # Find the StartFlow parameter that corresponds to this target
                for startflow_param_name, original_node_param in start_node_param_mappings.items():
                    if (
                        original_node_param.node_name == target_node_name
                        and original_node_param.parameter_name == target_param_name
                    ):
                        # This StartFlow parameter feeds the target - set the current_item value
                        if iteration_index < len(current_item_values):
                            iteration_values[startflow_param_name] = current_item_values[iteration_index]
                        break

            parameter_val_mappings[iteration_index] = iteration_values

        return parameter_val_mappings

    def _get_resolved_upstream_values(  # noqa: C901
        self,
        package_result: PackageNodesAsSerializedFlowResultSuccess,
    ) -> dict[str, Any]:
        """Collect parameter values from resolved upstream nodes outside the group.

        When nodes inside the group have connections to nodes outside that have already
        executed (RESOLVED state), we need to pass those values into the packaged flow
        via the StartFlow node parameters.

        Args:
            package_result: PackageNodesAsSerializedFlowResultSuccess containing parameter_name_mappings

        Returns:
            Dict mapping startflow_param_name -> value from resolved upstream node
        """
        from griptape_nodes.exe_types.node_types import NodeResolutionState

        flow_manager = GriptapeNodes.FlowManager()
        connections = flow_manager.get_connections()
        node_manager = GriptapeNodes.NodeManager()

        # Get Start node's parameter mappings (index 0 in the list)
        start_node_mapping = package_result.parameter_name_mappings[0]
        start_node_param_mappings = start_node_mapping.parameter_mappings

        packaged_node_names = package_result.packaged_node_names

        resolved_upstream_values: dict[str, Any] = {}

        # For each packaged node, check its incoming data connections
        for packaged_node_name in packaged_node_names:
            try:
                packaged_node = node_manager.get_node_by_name(packaged_node_name)
            except Exception:
                logger.warning("Could not find packaged node '%s' to check upstream connections", packaged_node_name)
                continue

            # Check each parameter for incoming connections
            for param in packaged_node.parameters:
                # Skip control parameters
                if param.type == ParameterTypeBuiltin.CONTROL_TYPE:
                    continue

                # Get upstream connection
                upstream_connection = connections.get_connected_node(packaged_node, param)
                if not upstream_connection:
                    continue

                upstream_node, upstream_param = upstream_connection

                # Skip if upstream node is inside the packaged group
                if upstream_node.name in packaged_node_names:
                    continue

                # Skip if upstream node is not resolved
                if upstream_node.state != NodeResolutionState.RESOLVED:
                    continue

                # Get the upstream value
                if upstream_param.name in upstream_node.parameter_output_values:
                    upstream_value = upstream_node.parameter_output_values[upstream_param.name]
                else:
                    upstream_value = upstream_node.get_parameter_value(upstream_param.name)

                if upstream_value is None:
                    continue

                # Find the corresponding StartFlow parameter name
                for startflow_param_name, original_node_param in start_node_param_mappings.items():
                    if (
                        original_node_param.node_name == packaged_node_name
                        and original_node_param.parameter_name == param.name
                    ):
                        resolved_upstream_values[startflow_param_name] = upstream_value
                        logger.debug(
                            "Collected resolved upstream value: %s.%s -> StartFlow.%s",
                            upstream_node.name,
                            upstream_param.name,
                            startflow_param_name,
                        )
                        break

        logger.info("Collected %d resolved upstream values for group execution", len(resolved_upstream_values))
        return resolved_upstream_values

    def _get_merged_parameter_values_for_iterations(
        self,
        package_result: PackageNodesAsSerializedFlowResultSuccess,
    ) -> dict[int, dict[str, Any]]:
        """Get parameter values for each iteration with resolved upstream values merged in.

        Args:
            package_result: The packaged flow result containing parameter mappings

        Returns:
            Dict mapping iteration_index -> {parameter_name: value}
        """
        # Get parameter values that vary per iteration (current_item mappings)
        parameter_values_per_iteration = self._get_parameter_values_per_iteration(package_result)

        # Get resolved upstream values (constant across all iterations)
        resolved_upstream_values = self._get_resolved_upstream_values(package_result)

        # Merge upstream values into each iteration (only if parameter doesn't already exist)
        if resolved_upstream_values:
            for iteration_index in parameter_values_per_iteration:
                for param_name, param_value in resolved_upstream_values.items():
                    if param_name not in parameter_values_per_iteration[iteration_index]:
                        parameter_values_per_iteration[iteration_index][param_name] = param_value
            logger.info(
                "Added %d resolved upstream values to %d iterations",
                len(resolved_upstream_values),
                len(parameter_values_per_iteration),
            )

        return parameter_values_per_iteration

    _START_FLOW_PARAM_PREFIX = "deadlinecloudstartflow"

    def _get_result_parameter_name(
        self,
        package_result: PackageNodesAsSerializedFlowResultSuccess,
    ) -> str | None:
        """Find the EndFlow parameter name that corresponds to new_item_to_add.

        The new_item_to_add parameter receives input from a node inside the group.
        When the workflow is packaged, that connection becomes an EndFlow parameter.
        We need to find that EndFlow parameter name to extract the correct result value.

        Args:
            package_result: PackageNodesAsSerializedFlowResultSuccess containing parameter_name_mappings

        Returns:
            The EndFlow parameter name that maps to new_item_to_add, or None if not found
        """
        from griptape_nodes.retained_mode.events.connection_events import (
            ListConnectionsForNodeRequest,
            ListConnectionsForNodeResultSuccess,
        )

        # Get incoming connections to this node's new_item_to_add parameter
        list_connections_request = ListConnectionsForNodeRequest(node_name=self.name)
        list_connections_result = GriptapeNodes.handle_request(list_connections_request)
        if not isinstance(list_connections_result, ListConnectionsForNodeResultSuccess):
            logger.warning("Failed to list connections for node %s", self.name)
            return None

        incoming_connections = list_connections_result.incoming_connections

        # Find the connection to new_item_to_add
        source_node_name = None
        source_param_name = None
        for conn in incoming_connections:
            if conn.target_parameter_name == "new_item_to_add":
                source_node_name = conn.source_node_name
                source_param_name = conn.source_parameter_name
                break

        if source_node_name is None or source_param_name is None:
            logger.info("No connection found to new_item_to_add parameter")
            return None

        # Get the End node's parameter mappings (index 1 in the list)
        # The end_node_param_mappings tells us: endflow_param_name -> OriginalNodeParameter(source_node, source_param)
        if len(package_result.parameter_name_mappings) < 2:  # noqa: PLR2004
            logger.warning("Package result does not have end node parameter mappings")
            return None

        end_node_mapping = package_result.parameter_name_mappings[1]
        end_node_param_mappings = end_node_mapping.parameter_mappings

        # Find the EndFlow parameter that corresponds to the source node/param
        for endflow_param_name, original_node_param in end_node_param_mappings.items():
            if (
                original_node_param.node_name == source_node_name
                and original_node_param.parameter_name == source_param_name
            ):
                logger.info(
                    "Found result parameter mapping: %s.%s -> EndFlow.%s",
                    source_node_name,
                    source_param_name,
                    endflow_param_name,
                )
                return endflow_param_name

        logger.warning(
            "Could not find EndFlow parameter for %s.%s",
            source_node_name,
            source_param_name,
        )
        return None

    def _get_start_flow_parameter_value(self, param_name: str, default: Any | None = None) -> Any:
        """Get a parameter value with the StartFlow node prefix.

        Parameters from the DeadlineCloudStartFlow node are added to this group
        with a prefix of the class name in lowercase (e.g., 'deadlinecloudstartflow_').

        Args:
            param_name: The original parameter name without prefix
            default: Default value to return if parameter is not set

        Returns:
            The parameter value
        """
        prefixed_name = f"{self._START_FLOW_PARAM_PREFIX}_{param_name}"
        value = self.get_parameter_value(prefixed_name)
        return value if value is not None else default

    def _build_host_requirements(self) -> dict[str, Any] | None:
        """Build host requirements dict from prefixed StartFlow parameters.

        Returns:
            Host requirements dict with 'amounts' and/or 'attributes', or None if
            run_on_all_worker_hosts is True or no requirements are configured.
        """
        from publish.parameters.deadline_cloud_host_config_parameter import DeadlineCloudHostConfigParameter

        amounts: list[dict[str, Any]] = []
        attributes: list[dict[str, Any]] = []

        # Build attribute requirements
        operating_system = self._get_start_flow_parameter_value("operating_system")
        if operating_system:
            attributes.append(
                {
                    "name": "attr.worker.os.family",
                    "anyOf": operating_system,
                }
            )

        cpu_architecture = self._get_start_flow_parameter_value("cpu_architecture")
        if cpu_architecture:
            attributes.append(
                {
                    "name": "attr.worker.cpu.arch",
                    "anyOf": cpu_architecture,
                }
            )

        # Build amount requirements using the classmethod helpers
        vcpu = self._get_start_flow_parameter_value("vcpu")
        vcpu_entry = DeadlineCloudHostConfigParameter._create_amount_entry("amount.worker.vcpu", vcpu, default_min=1)
        if vcpu_entry:
            amounts.append(vcpu_entry)

        memory = self._get_start_flow_parameter_value("memory")
        memory_entry = DeadlineCloudHostConfigParameter._create_amount_entry(
            "amount.worker.memory", memory, 1024, default_min=0
        )
        if memory_entry:
            amounts.append(memory_entry)

        gpus = self._get_start_flow_parameter_value("gpus")
        gpu_entry = DeadlineCloudHostConfigParameter._create_amount_entry("amount.worker.gpu", gpus, default_min=0)
        if gpu_entry:
            amounts.append(gpu_entry)

        gpu_memory = self._get_start_flow_parameter_value("gpu_memory")
        gpu_memory_entry = DeadlineCloudHostConfigParameter._create_amount_entry(
            "amount.worker.gpu.memory", gpu_memory, 1024, default_min=0
        )
        if gpu_memory_entry:
            amounts.append(gpu_memory_entry)

        scratch_space = self._get_start_flow_parameter_value("scratch_space")
        scratch_entry = DeadlineCloudHostConfigParameter._create_amount_entry(
            "amount.worker.scratch", scratch_space, 1024, default_min=0
        )
        if scratch_entry:
            amounts.append(scratch_entry)

        # Build host config dict
        host_config: dict[str, Any] = {}
        if amounts:
            host_config["amounts"] = amounts
        if attributes:
            host_config["attributes"] = attributes

        return host_config if host_config else None

    async def _arun(self) -> None:
        """Asynchronous execution of the multi-task group node."""
        from publish.deadline_cloud_multi_task_publisher import (
            DeadlineCloudMultiTaskPublisher,
            MultiTaskPublisherConfig,
        )

        # Initialize iteration data to determine total iterations
        self._initialize_iteration_data()

        total_iterations = self._get_total_iterations()
        if total_iterations == 0:
            logger.info("No iterations for empty loop")
            self.parameter_output_values["results"] = []
            return

        package_result = await self._package_group_body()
        if package_result is None:
            logger.info("No nodes in group to execute")
            self.parameter_output_values["results"] = []
            return

        # Get parameter values for each iteration
        parameter_values_per_iteration = self._get_merged_parameter_values_for_iterations(package_result)

        # Get the EndFlow parameter name that maps to new_item_to_add for result extraction
        result_parameter_name = self._get_result_parameter_name(package_result)

        # Get job submission parameters from this node (with StartFlow prefix)
        farm_id = self._get_start_flow_parameter_value("farm_id")
        queue_id = self._get_start_flow_parameter_value("queue_id")
        storage_profile_id = self._get_start_flow_parameter_value("storage_profile_id")
        job_name = self._get_start_flow_parameter_value("job_name", default=f"{self.name} Multi-Task Job")
        job_description = self._get_start_flow_parameter_value(
            "job_description", default=f"Multi-task job for {self.name}"
        )
        priority = self._get_start_flow_parameter_value("priority", default=50)
        initial_state = self._get_start_flow_parameter_value("initial_state", default="READY")
        max_failed_tasks = self._get_start_flow_parameter_value("max_failed_tasks", default=50)
        max_task_retries = self._get_start_flow_parameter_value("max_task_retries", default=10)
        attachment_input_paths = self._get_start_flow_parameter_value("attachment_input_paths", default=[])
        attachment_output_paths = self._get_start_flow_parameter_value("attachment_output_paths", default=[])

        # Build host requirements from host config parameters
        host_requirements: dict[str, Any] | None = None
        run_on_all_worker_hosts = self._get_start_flow_parameter_value("run_on_all_worker_hosts")
        if not run_on_all_worker_hosts:
            host_requirements = self._build_host_requirements()

        # Create publisher config
        config = MultiTaskPublisherConfig(
            workflow_name=self.name,
            parameter_values_per_iteration=parameter_values_per_iteration,
            package_result=package_result,
            farm_id=farm_id,
            queue_id=queue_id,
            storage_profile_id=storage_profile_id,
            job_name=job_name,
            job_description=job_description,
            priority=priority,
            initial_state=initial_state,
            max_failed_tasks=max_failed_tasks,
            max_task_retries=max_task_retries,
            attachment_input_paths=attachment_input_paths,
            attachment_output_paths=attachment_output_paths,
            pickle_control_flow_result=True,
            host_requirements=host_requirements,
            result_parameter_name=result_parameter_name,
        )

        # Create and execute the multi-task publisher
        publisher = DeadlineCloudMultiTaskPublisher(config)

        logger.info(
            "Starting multi-task execution for '%s' with %d iterations",
            self.name,
            total_iterations,
        )

        results = await publisher.publish_and_execute()

        logger.info(
            "Multi-task execution completed for '%s' with %d results",
            self.name,
            len(results),
        )

        # Store results in output parameter
        self.parameter_output_values["results"] = results

    async def aprocess(self) -> None:
        try:
            await self._arun()
        finally:
            self.set_parameter_value("execution_environment", LIBRARY_NAME)
