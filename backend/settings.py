"""
Settings module for the app.
"""

from enum import StrEnum, unique

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


@unique
class LogLevel(StrEnum):
    """
    This class represents the LogLevel enum.
    """

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class _Settings(BaseSettings):
    """
    Settings class for the app.
    """

    # Application Variables
    APPLICATION_NAME: str = Field(default=..., min_length=1)
    APPLICATION_HOST: str = Field(default=..., min_length=1)  # It can be an IP address or a domain name
    APPLICATION_PORT: int = Field(default=..., ge=0, le=65535)
    FRONTEND_URL: str = Field(default=..., min_length=1)
    LOG_LEVEL: LogLevel = Field(default=LogLevel.INFO, description="The logging level to use.")

    # Security Variables
    SECRET_KEY: str = Field(default=..., min_length=1)
    ACCESS_TOKEN_EXPIRATION_TIME: int = Field(default=..., ge=0)  # Time in seconds
    ACCESS_TOKEN_NOT_BEFORE_TIME: int = Field(default=..., ge=0)  # Time in seconds
    REFRESH_TOKEN_EXPIRATION_TIME: int = Field(default=..., ge=0)  # Time in seconds
    REFRESH_TOKEN_NOT_BEFORE_TIME: int = Field(default=..., ge=0)  # Time in seconds

    # Database Variables
    DATABASE_USERNAME: str = Field(default=..., min_length=1)
    DATABASE_PASSWORD: str = Field(default=..., min_length=1)
    DATABASE_HOST: str = Field(default=..., min_length=1)  # It can be an IP address or a domain name
    DATABASE_PORT: int = Field(default=..., ge=0, le=65535)
    DATABASE_NAME: str = Field(default=..., min_length=1)
    DATABASE_MINIMUM_CONNECTIONS: int = Field(default=..., ge=0)
    DATABASE_MAXIMUM_CONNECTIONS: int = Field(default=..., ge=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


Settings = _Settings()
