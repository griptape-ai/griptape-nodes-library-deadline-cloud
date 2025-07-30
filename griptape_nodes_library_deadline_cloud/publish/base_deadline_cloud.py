from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, TypeVar

import boto3
from deadline.client.api import get_boto3_session
from deadline.client.config import get_setting_default
from griptape_nodes.retained_mode.griptape_nodes import (
    GriptapeNodes,
)
from publish import DEADLINE_CLOUD_LIBRARY_CONFIG_KEY

if TYPE_CHECKING:
    from botocore.client import BaseClient


T = TypeVar("T")


logger = logging.getLogger("base_deadline_cloud")


class BaseDeadlineCloud:
    def __init__(self, session: boto3.Session | None = None) -> None:
        self._session = session if session is not None else self._get_session()
        self._client: BaseClient | None = None

    @classmethod
    def _get_session(cls) -> boto3.Session:
        """Get the boto3 session."""
        profile_name = cls._get_config_value(
            DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "profile_name", default=get_setting_default("defaults.aws_profile_name")
        )
        region_name = cls._get_config_value(DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "region_name", default="us-east-1")
        if profile_name != "" and region_name != "":
            return boto3.Session(profile_name=profile_name, region_name=region_name)

        return get_boto3_session()

    @classmethod
    def _get_config_value(cls, service: str, value: str, default: Any | None = None) -> Any:
        """Retrieves a configuration value from the ConfigManager."""
        config_value = GriptapeNodes.ConfigManager().get_config_value(f"{service}.{value}")
        if not config_value and default is None:
            details = f"Failed to get configuration value '{value}' for service '{service}'."
            logger.error(details)
            raise ValueError(details)
        return config_value or default

    @classmethod
    def _get_secret(cls, secret: str) -> str:
        """Retrieves a secret value from the SecretsManager."""
        secret_value = GriptapeNodes.SecretsManager().get_secret(secret)
        if not secret_value:
            details = f"Failed to get secret:'{secret}'."
            logger.error(details)
            raise ValueError(details)
        return secret_value

    def _get_client(self) -> BaseClient:
        """Get cached Deadline Cloud client."""
        if self._client is None:
            self._client = self._session.client(
                "deadline", region_name=self._get_config_value(DEADLINE_CLOUD_LIBRARY_CONFIG_KEY, "region_name")
            )
        return self._client
