"""
This module contains the refresh token schema.
"""

from pydantic import Field

from backend.shared.schemas import BaseRequestSchema


class RefreshTokenSchema(BaseRequestSchema):
    """
    Refresh token schema.
    """

    refresh_token: str = Field(
        default=...,
        serialization_alias='refreshToken',
        description='Refresh token.',
        examples=[
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoicmVmcmVzaCIsImlzcyI6InBhdGllbnQtaHViLWJhY2tlbmQiLCJzdWIiOiJkNzFhNjNlYi0zZDhkLTQyNTktYTAyNi00OWJiMmMzZDlmYTIiLCJhdWQiOiJwYXRpZW50LWh1Yi1iYWNrZW5kIiwiaWF0IjoxNzI2OTQxMDk5LCJleHAiOjE3Mjk1MzMwOTksIm5iZiI6MTcyNjk0MTA5OSwianRpIjoiNzFiNDRlOGMtMDJlYS00ZDEwLWJkZTYtOTIwYjAyZGYxY2U3In0.4E9YOy2WQdQhfdt8XFz_i_ikIMMAogHIT7Y7_FsLuLo'
        ],
    )
