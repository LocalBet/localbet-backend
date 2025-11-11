"""
This module contains the MaxPayloadLengthMiddleware class, which checks if the request payload exceeds a maximum allowed
length.
"""

from typing_extensions import override

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class MaxPayloadLengthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks if the request payload exceeds a maximum allowed length.
    If the payload exceeds the maximum allowed length it returns a 413 Request Entity Too Large error.
    """

    __MAX_PAYLOAD_LENGTH = 1024 * 100  # 100 KB

    def __init__(self, app: ASGIApp) -> None:
        """
        MaxPayloadLengthMiddleware constructor.

        Args:
            app (ASGIApp): The ASGI app to wrap.
        """
        super().__init__(app=app)

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Middleware that checks the payload length of incoming requests.

        Args:
            request (Request): The request that the user is making.
            call_next (RequestResponseEndpoint): The next middleware or endpoint to call.

        Returns:
            Response: The HTTP response.
        """
        body_length = len(await request.body())

        if body_length > self.__MAX_PAYLOAD_LENGTH:
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={
                    "error": {
                        "title": "Payload Too Large",
                        "message": f"Payload exceeds the maximum size of {self.__MAX_PAYLOAD_LENGTH / (1024)} KB.",
                    }
                },
            )

        return await call_next(request)
