import logging

from griptape_nodes.exe_types.node_types import AsyncResult, ControlNode

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DeadlineCloudPublishedWorkflow(ControlNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        metadata = kwargs.get("metadata", {})

        # Store workflow shape and structure info
        self.workflow_shape = metadata.get("workflow_shape", {})

    def _process(self) -> None:
        return

    def process(
        self,
    ) -> AsyncResult[None]:
        yield lambda: None
        self._process()
