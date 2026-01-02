"""
APP Module.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import Logger, basicConfig, getLogger

from backend.services.redis import redis_client

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.auth.endpoints import router as auth_router
from backend.database import pool
from backend.db_init import init_db
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
from backend.bets.endpoints import router as bets_router
from backend.groups.endpoints import router as groups_router
from backend.stats.endpoints import router as stats_router

# Logging configuration
LOGGER: Logger = getLogger(__name__)
basicConfig(
    level=Settings.LOG_LEVEL,
    format="%(asctime)s <%(name)s> [%(levelname)s] %(message)s",
)


# Fast API + Redis
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    Context manager to open and close the database connection pool
    and initialize database schema.
    """
    pool.open()

    # ✅ Inicialitza la base de dades (crea taules si no existeixen)
    # init_db()

    # Verifica conexión con Redis
    await redis_client.ping()

    yield

    pool.close()
    await redis_client.close()


app = FastAPI(
    title=Settings.APPLICATION_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan,
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # puedes usar ["*"] para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(router=auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(router=users_router, prefix="/users", tags=["Users"])
app.include_router(router=bets_router, prefix="/bets", tags=["Bets"])
app.include_router(router=groups_router, prefix="/groups", tags=["Groups"])
app.include_router(router=stats_router, prefix="/stats", tags=["Statistics"])

# Middlewares
app.add_middleware(MaxUriLengthMiddleware)
app.add_middleware(MaxHeaderLengthMiddleware)
app.add_middleware(MaxPayloadLengthMiddleware)
app.add_middleware(ContentTypeMiddleware)
app.add_middleware(AcceptHeaderMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Settings.FRONTEND_URL],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization"],
    allow_credentials=True,
    max_age=600,
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
    return f"Welcome to {Settings.APPLICATION_NAME} API. For more information please refer to /docs"


# ---------- Exception Handlers ----------

@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request, exception: RequestValidationError
) -> JSONResponse:
    for error in exception.errors():
        if isinstance(error, dict) and "msg" in error:
            break

        if error.get("type") == "missing" and error.get("loc", [None])[0] == "body":
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
            error.get("type") == "enum"
            and error.get("loc", [None])[0] == "body"
            and "msg" in error
        ):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": {
                        "title": "Bad Request",
                        "message": (
                            f"The request body contains an invalid value for "
                            f"'{error['loc'][1]}'. {error['msg']}"
                        ),
                    },
                },
            )

    raise exception


@app.exception_handler(MissingFieldsError)
async def handle_missing_fields_error(
    request: Request, exception: MissingFieldsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "title": "Bad Request",
                "message": exception.message,
            },
        },
    )


@app.exception_handler(ExtraFieldsError)
async def handle_extra_fields_error(
    request: Request, exception: ExtraFieldsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "title": "Bad Request",
                "message": exception.message,
            },
        },
    )


@app.exception_handler(HTTPError)
async def handle_app_errors(
    request: Request, exception: HTTPError
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "title": exception.title,
                "message": exception.message,
            }
        },
    )


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def handle_not_found_error(
    request: Request, exception: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "title": "Not Found",
                "message": "The requested resource was not found.",
                "details": {
                    "method": str(request.method),
                    "url": str(request.url.path),
                },
            }
        },
    )


@app.exception_handler(status.HTTP_405_METHOD_NOT_ALLOWED)
async def handle_method_not_allowed_error(
    request: Request, exception: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "title": "Method not Allowed",
                "message": "The requested method is not allowed for the requested URL.",
                "details": {
                    "method": str(request.method),
                    "url": str(request.url.path),
                },
            }
        },
    )
