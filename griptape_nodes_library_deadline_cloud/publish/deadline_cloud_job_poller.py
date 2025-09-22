from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable
    from configparser import ConfigParser

    from botocore.client import BaseClient


logger = logging.getLogger(__name__)


class LifecycleStatus(StrEnum):
    """Lifecycle status values for Deadline Cloud jobs."""

    CREATE_IN_PROGRESS = "CREATE_IN_PROGRESS"
    CREATE_FAILED = "CREATE_FAILED"
    CREATE_COMPLETE = "CREATE_COMPLETE"
    UPLOAD_IN_PROGRESS = "UPLOAD_IN_PROGRESS"
    UPLOAD_FAILED = "UPLOAD_FAILED"
    UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
    UPDATE_FAILED = "UPDATE_FAILED"
    UPDATE_SUCCEEDED = "UPDATE_SUCCEEDED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def get_failed_statuses(cls) -> list[LifecycleStatus]:
        """Get the list of lifecycle statuses that indicate failure."""
        return [cls.CREATE_FAILED, cls.UPLOAD_FAILED, cls.UPDATE_FAILED, cls.ARCHIVED]


class TaskRunStatus(StrEnum):
    """Task run status values for Deadline Cloud jobs."""

    PENDING = "PENDING"
    READY = "READY"
    ASSIGNED = "ASSIGNED"
    STARTING = "STARTING"
    SCHEDULED = "SCHEDULED"
    INTERRUPTING = "INTERRUPTING"
    RUNNING = "RUNNING"
    SUSPENDED = "SUSPENDED"
    CANCELED = "CANCELED"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"
    NOT_COMPATIBLE = "NOT_COMPATIBLE"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def get_completed_statuses(cls) -> list[TaskRunStatus]:
        """Get the list of task run statuses that indicate completion."""
        return [cls.SUCCEEDED, cls.FAILED, cls.CANCELED, cls.NOT_COMPATIBLE]


@dataclass
class DeadlineCloudJobDetails:
    """Job details from Deadline Cloud with key timestamps, statuses, and metadata.

    Attributes:
        job_id (str): The ID of the job.
        name (str): The name of the job.
        description (str | None): The description of the job.
        lifecycle_status (LifecycleStatus): The lifecycle status of the job.
        lifecycle_status_message (str | None): Message associated with the lifecycle status.
        task_run_status (TaskRunStatus): The task run status of the job.
        priority (int): The priority of the job.
        created_at (str): When the job was created.
        created_by (str): Who created the job.
        started_at (str | None): When the job started.
        ended_at (str | None): When the job ended.
        updated_at (str): When the job was last updated.
        updated_by (str): Who last updated the job.
        max_failed_tasks_count (int): Maximum number of failed tasks allowed.
        max_retries_per_task (int): Maximum retries per task.
        task_failure_retry_count (int): Current task failure retry count.
        storage_profile_id (str | None): The storage profile ID.
        source_job_id (str | None): The source job ID if this is a retry.
    """

    job_id: str
    name: str
    description: str | None
    lifecycle_status: LifecycleStatus
    lifecycle_status_message: str | None
    task_run_status: TaskRunStatus
    priority: int
    created_at: str
    created_by: str
    started_at: str | None
    ended_at: str | None
    updated_at: str
    updated_by: str
    max_failed_tasks_count: int
    max_retries_per_task: int
    task_failure_retry_count: int
    storage_profile_id: str | None
    source_job_id: str | None

    @classmethod
    def from_job_details(cls, job_details: dict[str, Any]) -> DeadlineCloudJobDetails:
        """Create a DeadlineCloudJobDetails instance from a job details dictionary.

        Args:
            job_details: Dictionary containing job details from AWS Deadline Cloud API.

        Returns:
            DeadlineCloudJobDetails instance with populated fields.
        """
        return cls(
            job_id=job_details.get("jobId", ""),
            name=job_details.get("name", ""),
            description=job_details.get("description"),
            lifecycle_status=LifecycleStatus(job_details.get("lifecycleStatus", "UNKNOWN")),
            lifecycle_status_message=job_details.get("lifecycleStatusMessage"),
            task_run_status=TaskRunStatus(job_details.get("taskRunStatus", "UNKNOWN")),
            priority=job_details.get("priority", 0),
            created_at=job_details.get("createdAt", ""),
            created_by=job_details.get("createdBy", ""),
            started_at=job_details.get("startedAt"),
            ended_at=job_details.get("endedAt"),
            updated_at=job_details.get("updatedAt", ""),
            updated_by=job_details.get("updatedBy", ""),
            max_failed_tasks_count=job_details.get("maxFailedTasksCount", 0),
            max_retries_per_task=job_details.get("maxRetriesPerTask", 0),
            task_failure_retry_count=job_details.get("taskFailureRetryCount", 0),
            storage_profile_id=job_details.get("storageProfileId"),
            source_job_id=job_details.get("sourceJobId"),
        )


class DeadlineCloudJobPoller:
    """Polls the Deadline Cloud job until completion.

    Attributes:
        client (BaseClient): The Deadline Cloud client.
        job_id (str): The ID of the job to poll.
        queue_id (str): The ID of the queue where the job is submitted.
        farm_id (str): The ID of the farm where the job is submitted.
        max_poll_interval (int): Maximum time to wait between polls in seconds.
        status_callback (Callable[[DeadlineCloudJobDetails, float], None] | None): Optional callback function to report status updates.
    """

    def __init__(  # noqa: PLR0913
        self,
        client: BaseClient,
        config: ConfigParser,
        job_id: str,
        queue_id: str,
        farm_id: str,
        max_poll_interval: int = 120,
        status_callback: Callable[[DeadlineCloudJobDetails, float], None] | None = None,
    ) -> None:
        self.client = client
        self.config = config
        self.job_id = job_id
        self.queue_id = queue_id
        self.farm_id = farm_id
        self.max_poll_interval = max_poll_interval
        self.status_callback = status_callback

    def poll_job(self) -> Any:
        """Poll the job until completion and return job details.

        Args:
            max_poll_interval: Maximum time to wait between polls in seconds.
        """
        job_details_dict: Any = {}
        current_job_details: DeadlineCloudJobDetails | None = None
        failed_statuses = LifecycleStatus.get_failed_statuses()

        # Exponential backoff parameters
        poll_interval = 0.5  # Start with 0.5 seconds
        backoff_multiplier = 1.5
        max_interval = float(self.max_poll_interval)
        poll_count = 0
        start_time = time.time()

        while True:
            poll_count += 1
            job_details_dict = self.client.get_job(jobId=self.job_id, queueId=self.queue_id, farmId=self.farm_id)
            current_job_details = DeadlineCloudJobDetails.from_job_details(job_details_dict)

            elapsed_time = time.time() - start_time

            if self.status_callback:
                self.status_callback(current_job_details, elapsed_time)

            logger.info(
                "Job %s poll #%d - Lifecycle: %s, Task Status: %s (elapsed: %.1fs)",
                self.job_id,
                poll_count,
                current_job_details.lifecycle_status,
                current_job_details.task_run_status,
                elapsed_time,
            )

            # Check for failure conditions
            if current_job_details.lifecycle_status in failed_statuses:
                break

            # Check for completion
            if current_job_details.task_run_status in TaskRunStatus.get_completed_statuses():
                break

            # Sleep with exponential backoff
            logger.debug("Waiting %.1f seconds before next poll", poll_interval)
            time.sleep(poll_interval)

            # Increase poll interval with backoff, but cap at max_interval
            poll_interval = min(poll_interval * backoff_multiplier, max_interval)

        if current_job_details and current_job_details.lifecycle_status in failed_statuses:
            msg = f"Job {self.job_id} failed with lifecycle status: {current_job_details.lifecycle_status}"
            logger.error(msg)
            raise RuntimeError(msg)

        if current_job_details and current_job_details.task_run_status != TaskRunStatus.SUCCEEDED:
            msg = f"Job {self.job_id} did not complete successfully. Final task run status: {current_job_details.task_run_status}"
            logger.error(msg)
            raise RuntimeError(msg)

        logger.info("Job %s completed successfully after %d polls (%.1fs)", self.job_id, poll_count, elapsed_time)
        return job_details_dict
