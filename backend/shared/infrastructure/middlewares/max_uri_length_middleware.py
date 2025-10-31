"""
This module contains the MaxUriLengthMiddleware class, which checks if the request uri exceeds a maximum allowed length.
"""

from typing_extensions import override

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class MaxUriLengthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks if the request uri exceeds a maximum allowed length.
    If the uri length exceeds the maximum allowed length it returns a 414 URI Too Long error.
    """

    __MAX_URI_LENGTH: int = 2048

    def __init__(self, app: ASGIApp) -> None:
        """
        URILengthMiddleware constructor.

        Args:
            app (ASGIApp): The ASGI app to wrap.
        """
        super().__init__(app=app)

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Middleware that checks the uri length of incoming requests.

        Args:
            call_next (Request): The request that the user is making.
            endpoint (RequestResponseEndpoint): The next middleware or endpoint to call.

        Returns:
            Response: The HTTP response.
        """
        uri_length = len(str(object=request.url))

        if uri_length > self.__MAX_URI_LENGTH:
            return JSONResponse(
                status_code=status.HTTP_414_REQUEST_URI_TOO_LONG,
                content={
                    'error': {
                        'title': 'URI Too Long',
                        'message': f'The URI length exceeds {self.__MAX_URI_LENGTH} bytes.',
                    }
                },
            )

        return await call_next(request)
