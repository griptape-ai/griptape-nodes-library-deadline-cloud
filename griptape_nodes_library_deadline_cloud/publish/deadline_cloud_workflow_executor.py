import json
import logging
from pathlib import Path

from griptape_nodes.bootstrap.workflow_executors.local_workflow_executor import LocalWorkflowExecutor
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DeadlineCloudWorkflowExecutor(LocalWorkflowExecutor):
    def _submit_output(self, output: dict) -> None:
        logger.info("Submitting output to Deadline Cloud: %s", output)

        workspace_directory = GriptapeNodes.ConfigManager().get_config_value("workspace_directory")
        workspace_directory_path = Path(workspace_directory)
        output_json_path = workspace_directory_path / "workflow_output.json"
        with output_json_path.open("w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
