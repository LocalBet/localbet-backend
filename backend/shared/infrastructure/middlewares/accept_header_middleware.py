"""
This module contains the AcceptHeaderMiddleware class, which checks the 'Accept' header of incoming requests.
"""

from typing import ClassVar
from typing_extensions import override

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class AcceptHeaderMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks the 'Accept' header and ensures the request can be satisfied.
    If not, it returns a 406 Not Acceptable response.
    """

    __ACCEPTABLE_CONTENT_TYPES: ClassVar[set[str]] = {
        '*/*',
        'application/json',
    }

    def __init__(self, app: ASGIApp) -> None:
        """
        AcceptHeaderMiddleware constructor.

        Args:
            app (ASGIApp): The ASGI app to wrap.
        """
        super().__init__(app=app)

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Check the Accept header and ensure the request can be fulfilled.
        If the Accept header is unsupported, return 406 Not Acceptable.

        Args:
            request (Request): The request that the user is making.
            call_next (RequestResponseEndpoint): The next middleware or endpoint to call.

        Returns:
            Response: The HTTP response.
        """
        accept_header = request.headers.get('Accept', 'application/json').split(',')
        accept_header = [accept_type.split(';')[0].strip() for accept_type in accept_header]

        if not any(accept_type in self.__ACCEPTABLE_CONTENT_TYPES for accept_type in accept_header):
            return JSONResponse(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                content={
                    'error': {
                        'title': 'Not Acceptable',
                        'message': f"Accept header '{accept_header}' is not supported. Supported types: {', '.join(self.__ACCEPTABLE_CONTENT_TYPES)}",  # noqa: E501
                    }
                },
            )

        return await call_next(request)
