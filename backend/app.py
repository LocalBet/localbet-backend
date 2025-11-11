"""
APP Module.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import Logger, basicConfig, getLogger

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.auth.endpoints import router as auth_router
from backend.database import pool
from backend.settings import Settings
from backend.shared.infrastructure.errors import ExtraFieldsError, HTTPError, MissingFieldsError
from backend.shared.infrastructure.middlewares import (
    AcceptHeaderMiddleware,
    ContentTypeMiddleware,
    MaxHeaderLengthMiddleware,
    MaxPayloadLengthMiddleware,
    MaxUriLengthMiddleware,
)
from backend.users.endpoints import router as users_router

# Logging configuration
LOGGER: Logger = getLogger(__name__)
basicConfig(level=Settings.LOG_LEVEL, format="%(asctime)s <%(name)s> [%(levelname)s] %(message)s")


# Fast API
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    Context manager to open and close the database connection pool.

    Args:
        app (CustomFastAPI): The FastAPI application instance.
    """
    pool.open()

    yield

    pool.close()


app = FastAPI(title=Settings.APPLICATION_NAME, version="1.0.0", docs_url="/docs", redoc_url=None, lifespan=lifespan)

app.include_router(router=auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(router=users_router, prefix="/users", tags=["Users"])

app.add_middleware(middleware_class=MaxUriLengthMiddleware)
app.add_middleware(middleware_class=MaxHeaderLengthMiddleware)
app.add_middleware(middleware_class=MaxPayloadLengthMiddleware)
app.add_middleware(middleware_class=ContentTypeMiddleware)
app.add_middleware(middleware_class=AcceptHeaderMiddleware)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=[Settings.FRONTEND_URL],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization"],
    allow_credentials=True,
    max_age=600,  # 10 minutes
)


@app.get(
    path="/",
    tags=["General"],
    summary="Root endpoint.",
    description="Get a welcome message.",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def welcome() -> str:
    """
    Get a welcome message.

    Returns:
        MessageSchema: Welcome message.
    """
    return f"Welcome to {Settings.APPLICATION_NAME} API. For more information please refer to /docs"


@app.exception_handler(exc_class_or_status_code=RequestValidationError)
async def request_validation_error_handler(request: Request, exception: RequestValidationError) -> JSONResponse:
    """
    Handle request validation errors and convert them to HTTP error responses.

    Args:
        request (Request): The incoming HTTP request that triggered the exception.
        exception (RequestValidationError): The RequestValidationError exception instance containing the error details.

    Returns:
        JSONResponse: A JSON response with the appropriate HTTP status code and error message.
    """
    for error in exception.errors():
        if isinstance(error, dict) and "msg" in error:
            break

        if "type" in error and error["type"] == "missing":  # noqa: SIM102
            if "loc" in error and error["loc"][0] == "body":
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": {
                            "title": "Bad Request",
                            "message": "The request body is missing.",
                        },
                    },
                )

        if (
            "type" in error
            and error["type"] == "enum"
            and "loc" in error
            and error["loc"][0] == "body"
            and "msg" in error
        ):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": {
                        "title": "Bad Request",
                        "message": (
                            f"The request body contains an invalid value for '{error['loc'][1]}'. {error['msg']}"
                        ),
                    },
                },
            )

    raise exception


@app.exception_handler(exc_class_or_status_code=MissingFieldsError)
async def handle_missing_fields_error(request: Request, exception: MissingFieldsError) -> JSONResponse:
    """
    Handle missing fields errors and convert them to HTTP error responses.

    Args:
        request (Request): The incoming HTTP request that triggered the exception.
        exception (MissingFieldsError): The MissingFieldsError exception instance containing the error details.

    Returns:
        JSONResponse: A JSON response with the appropriate HTTP status code and error message.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "title": "Bad Request",
                "message": exception.message,
            },
        },
    )


@app.exception_handler(exc_class_or_status_code=ExtraFieldsError)
async def handle_extra_fields_error(request: Request, exception: ExtraFieldsError) -> JSONResponse:
    """
    Handle extra fields errors and convert them to HTTP error responses.

    Args:
        request (Request): The incoming HTTP request that triggered the exception.
        exception (ExtraFieldsError): The ExtraFieldsError exception instance containing the error details.

    Returns:
        JSONResponse: A JSON response with the appropriate HTTP status code and error message.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "title": "Bad Request",
                "message": exception.message,
            },
        },
    )


@app.exception_handler(exc_class_or_status_code=HTTPError)
async def handle_app_errors(request: Request, exception: HTTPError) -> JSONResponse:
    """
    Handle HTTPError exceptions and convert them to HTTP error responses.

    Args:
        request (Request): The incoming HTTP request that triggered the exception.
        exception (HTTPError): The HTTPError exception instance containing the error details.

    Returns:
        JSONResponse: A JSON response with the appropriate HTTP status code and error message.
    """
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "title": exception.title,
                "message": exception.message,
            }
        },
    )


@app.exception_handler(exc_class_or_status_code=status.HTTP_404_NOT_FOUND)
async def handle_not_found_error(request: Request, exception: HTTPException) -> JSONResponse:
    """
    Handle not found errors and convert them to HTTP error responses.

    Args:
        request (Request): The incoming HTTP request that triggered the exception.
        exception (HTTPError): The HTTPError exception instance containing the error details.

    Returns:
        JSONResponse: A JSON response with the appropriate HTTP status code and error message.
    """
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "title": "Not Found",
                "message": "The requested resource was not found.",
                "details": {
                    "method": str(object=request.method),
                    "url": str(object=request.url.path),
                },
            }
        },
    )


@app.exception_handler(exc_class_or_status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
async def handle_method_not_allowed_error(request: Request, exception: HTTPException) -> JSONResponse:
    """
    Handle method not allowed errors and convert them to HTTP error responses.

    Args:
        request (Request): The incoming HTTP request that triggered the exception.
        exception (HTTPError): The HTTPError exception instance containing the error details.

    Returns:
        JSONResponse: A JSON response with the appropriate HTTP status code and error message.
    """
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "title": "Method not Allowed",
                "message": "The requested method is not allowed for the requested URL.",
                "details": {
                    "method": str(object=request.method),
                    "url": str(object=request.url.path),
                },
            }
        },
    )
