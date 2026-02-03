import json
import logging
from pathlib import Path
from typing import Any

from griptape_nodes.bootstrap.workflow_executors.local_workflow_executor import LocalWorkflowExecutor
from griptape_nodes.retained_mode.events.parameter_events import SetParameterValueRequest
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DeadlineCloudWorkflowExecutor(LocalWorkflowExecutor):
    def __init__(
        self,
        *args: Any,
        location_to_remap: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._location_to_remap = location_to_remap

    def _submit_output(self, output: dict) -> None:
        self.output = output
        logger.info("Submitting output to Deadline Cloud: %s", output)

        workspace_directory = GriptapeNodes.ConfigManager().get_config_value("workspace_directory")
        workspace_directory_path = Path(workspace_directory)
        output_json_path = workspace_directory_path / "workflow_output.json"
        with output_json_path.open("w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)

    def _load_static_file_mappings(self) -> dict[str, dict[str, str]]:
        """Load static file mappings from the assets directory if they exist."""
        if self._location_to_remap is None:
            return {}

        mappings_path = Path(self._location_to_remap) / "assets" / "static_file_mappings.json"
        if not mappings_path.exists():
            logger.debug("No static file mappings found at %s", mappings_path)
            return {}

        try:
            with mappings_path.open("r", encoding="utf-8") as f:
                mappings = json.load(f)
        except Exception as e:
            logger.warning("Failed to load static file mappings: %s", e)
            return {}
        else:
            logger.info("Loaded static file mappings: %s", mappings)
            return mappings

    def _build_full_static_path(self, relative_path: str) -> str:
        """Build the full path for a static file on the Deadline worker."""
        if self._location_to_remap is None:
            return relative_path
        # Normalize Windows backslashes to forward slashes for cross-platform compatibility
        normalized_relative = relative_path.replace("\\", "/")
        return str(Path(self._location_to_remap) / "assets" / "static_files" / normalized_relative)

    async def _set_input_for_flow(self, flow_name: str, flow_input: dict[str, dict]) -> None:
        """Override to handle static file path substitution before normal input handling.

        This method:
        1. Loads the static file mappings from the assets directory
        2. Applies path substitutions for any node/parameter that needs remapping
        3. Removes substituted parameters from flow_input to prevent parent from overwriting
        4. Calls the parent implementation for normal StartNode input handling
        """
        # Load static file mappings
        static_file_mappings = self._load_static_file_mappings()

        if static_file_mappings:
            control_flow = GriptapeNodes.FlowManager().get_flow_by_name(flow_name)
            nodes = control_flow.nodes

            # Apply path substitutions for mapped parameters
            for node_name, param_mappings in static_file_mappings.items():
                node = nodes.get(node_name)
                if node is None:
                    logger.warning("Node '%s' from static file mappings not found in flow", node_name)
                    continue

                for param_name, relative_path in param_mappings.items():
                    full_path = self._build_full_static_path(relative_path)
                    logger.info(
                        "Substituting static file path for %s.%s: %s",
                        node_name,
                        param_name,
                        full_path,
                    )

                    set_parameter_value_request = SetParameterValueRequest(
                        parameter_name=param_name,
                        value=full_path,
                        node_name=node_name,
                    )
                    result = await GriptapeNodes.ahandle_request(set_parameter_value_request)

                    if result.failed():
                        logger.error(
                            "Failed to set static file path for %s.%s: %s",
                            node_name,
                            param_name,
                            result,
                        )
                    # Remove from flow_input to prevent parent from overwriting our substitution
                    elif node_name in flow_input and param_name in flow_input[node_name]:
                        del flow_input[node_name][param_name]
                        logger.debug(
                            "Removed %s.%s from flow_input to prevent overwrite",
                            node_name,
                            param_name,
                        )

        # Call parent implementation for normal StartNode input handling
        await super()._set_input_for_flow(flow_name, flow_input)
