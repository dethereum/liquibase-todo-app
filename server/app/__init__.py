"""FastAPI application factory and lifespan wiring."""

from __future__ import annotations

from contextlib import asynccontextmanager

import anyio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Database
from .routes import api_router
from .settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the FastAPI application configured with DB and middleware."""
    settings = settings or Settings.from_env()
    database = Database(settings)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            yield
        finally:
            await anyio.to_thread.run_sync(database.close)

    app = FastAPI(lifespan=lifespan)
    app.state.db = database

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(api_router)

    return app


app = create_app()
