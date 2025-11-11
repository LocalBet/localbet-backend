"""
This module contains the ContentTypeMiddleware class, which checks the content type of incoming requests.
"""

from typing import ClassVar
from typing_extensions import override

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class ContentTypeMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks the content type of incoming requests.
    If the content type is not supported it returns a 415 Unsupported Media Type error.
    """

    __ALLOWED_CONTENT_TYPES: ClassVar[set[str]] = {
        "application/json",
    }

    def __init__(self, app: ASGIApp) -> None:
        """
        ContentTypeMiddleware constructor.

        Args:
            app (ASGIApp): The ASGI app to wrap.
        """
        super().__init__(app=app)

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Middleware that checks the content type of incoming requests.

        Args:
            request (Request): The request that the user is making.
            call_next (RequestResponseEndpoint): The next middleware or endpoint to call.

        Returns:
            Response: The HTTP response.
        """
        content_type = request.headers.get("Content-Type")
        if content_type is None:
            return await call_next(request)

        if content_type not in self.__ALLOWED_CONTENT_TYPES:
            return JSONResponse(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                content={
                    "error": {
                        "title": "Unsupported Media Type",
                        "message": f"Content type '{content_type}' is not supported. Allowed types: {', '.join(self.__ALLOWED_CONTENT_TYPES)}",  # noqa: E501
                    }
                },
            )

        return await call_next(request)
