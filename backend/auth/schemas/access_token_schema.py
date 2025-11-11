"""
This module contains the access token schema.
"""

from pydantic import BaseModel, Field


class AccessTokenSchema(BaseModel):
    """
    Access token schema.
    """

    token_type: str = Field(
        default="Bearer",
        serialization_alias="tokenType",
        description="Token type.",
        examples=["Bearer"],
    )

    access_token: str = Field(
        default=...,
        serialization_alias="accessToken",
        description="Access token.",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaXNzIjoicGF0aWVudC1odWItYmFja2VuZCIsInN1YiI6ImQ3MWE2M2ViLTNkOGQtNDI1OS1hMDI2LTQ5YmIyYzNkOWZhMiIsImF1ZCI6InBhdGllbnQtaHViLWJhY2tlbmQiLCJpYXQiOjE3MjY5NDEwOTksImV4cCI6MTcyNjk0MTM5OSwibmJmIjoxNzI2OTQxMDk5LCJqdGkiOiI3ODhlZjk3My04NDk1LTRkZmYtYWMyOC0wMzM3MGFjMjhiOGQifQ.4o_XCRAf2uO-ToFBBRwl3nglURQPOow1XtexewQCx_4"
        ],
    )

    refresh_token: str = Field(
        default=...,
        serialization_alias="refreshToken",
        description="Refresh token.",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoicmVmcmVzaCIsImlzcyI6InBhdGllbnQtaHViLWJhY2tlbmQiLCJzdWIiOiJkNzFhNjNlYi0zZDhkLTQyNTktYTAyNi00OWJiMmMzZDlmYTIiLCJhdWQiOiJwYXRpZW50LWh1Yi1iYWNrZW5kIiwiaWF0IjoxNzI2OTQxMDk5LCJleHAiOjE3Mjk1MzMwOTksIm5iZiI6MTcyNjk0MTA5OSwianRpIjoiNzFiNDRlOGMtMDJlYS00ZDEwLWJkZTYtOTIwYjAyZGYxY2U3In0.4E9YOy2WQdQhfdt8XFz_i_ikIMMAogHIT7Y7_FsLuLo"
        ],
    )
