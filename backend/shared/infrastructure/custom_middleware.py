"""
This module contains a custom middleware wrapper that allows to add middlewares to FastAPI routes.
"""

from fastapi.routing import APIRoute
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


def MiddlewareWrapper(
    middlewares: list[Middleware | type[BaseHTTPMiddleware]] | None = None,
) -> type[APIRoute]:  # noqa: N802
    """
    Custom middleware wrapper that allows to add middlewares to FastAPI routes.

    Args:
        middlewares (list[Middleware | type[BaseHTTPMiddleware]], optional): List of middlewares to add to the FastAPI
        route. Defaults to [].
    """

    class CustomAPIRoute(APIRoute):
        """
        Custom API route that allows to add middlewares to FastAPI routes.
        """

        def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
            """
            Custom API route constructor.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
            """
            super().__init__(*args, **kwargs)
            app = self.app

            _middlewares = []
            for middleware in middlewares or []:
                if isinstance(middleware, Middleware):
                    _middlewares.append(middleware)
                else:
                    _middlewares.append((middleware, {}))  # type: ignore[arg-type]

            for cls, options in reversed(_middlewares):
                app = cls(app=app, **options)

            self.app = app

    return CustomAPIRoute
