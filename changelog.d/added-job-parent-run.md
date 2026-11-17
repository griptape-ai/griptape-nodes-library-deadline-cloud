- Spend from a Deadline Cloud job now counts toward the workflow run that started it, so that run's
  total in Griptape Cloud includes it. This covers a node group whose execution environment is AWS
  Deadline Cloud Library, the **Deadline Cloud Published Workflow** node, and the **Deadline Cloud
  Multi Task Group**. A workflow published before this version still runs, but its spend stays
  separate until it is published again.
  [#114](https://github.com/griptape-ai/griptape-nodes-library-deadline-cloud/issues/114)
