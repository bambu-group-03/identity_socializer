from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from identity_socializer.web.api.router import api_router
from identity_socializer.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)

APP_ROOT = Path(__file__).parent.parent

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:3000", # backoffice localhost
    # "http://next-app:3000", # backoffice docker microservice network
    # "http://localhost:9000", # content
    # NOT WORK IN DOCKER 🥺😥
    "*",
]


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="identity_socializer",
        version=metadata.version("identity_socializer"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    return app
