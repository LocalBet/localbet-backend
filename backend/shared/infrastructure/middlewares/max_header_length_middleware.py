"""
This module contains the MaxHeaderLengthMiddleware class, which checks if the request headers exceed a maximum allowed
length.
"""

from typing_extensions import override

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class MaxHeaderLengthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks if the request headers exceed a maximum allowed length.
    If the headers exceed the maximum allowed length it returns a 431 Request Header Fields Too Large error.
    """

    __MAX_HEADER_LENGTH = 8192  # Define a maximum header size in bytes

    def __init__(self, app: ASGIApp) -> None:
        """
        MaxHeaderLengthMiddleware constructor.

        Args:
            app (ASGIApp): The ASGI app to wrap.
        """
        super().__init__(app=app)

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Middleware that checks the header length of incoming requests.

        Args:
            request (Request): The request that the user is making.
            call_next (RequestResponseEndpoint): The next middleware or endpoint to call.

        Returns:
            Response: The HTTP response.
        """
        header_size = sum(len(key) + len(value) for key, value in request.headers.items())

        if header_size > self.__MAX_HEADER_LENGTH:
            return JSONResponse(
                status_code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
                content={
                    "error": {
                        "title": "Request Header Fields Too Large",
                        "message": f"Header size exceeds {self.__MAX_HEADER_LENGTH} bytes.",
                    }
                },
            )

        return await call_next(request)
