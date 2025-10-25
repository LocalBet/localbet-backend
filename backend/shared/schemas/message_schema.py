"""
This module contains the Pydantic schema for the message response.
"""

from pydantic import BaseModel, ConfigDict, Field


class MessageSchema(BaseModel):
    """
    Basic message response schema.
    """

    message: str = Field(
        default=...,
        description="The message to be displayed.",
        examples=["Welcome to my project API. For more information please refer to /docs."],
    )

    model_config = ConfigDict(extra="forbid")
