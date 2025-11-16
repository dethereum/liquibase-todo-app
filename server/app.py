from __future__ import annotations

import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg import conninfo
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, Field, field_validator
from starlette.responses import Response


@dataclass
class Settings:
    client_origin: str = "*"
    database_url: Optional[str] = None
    node_env: Optional[str] = None
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_database: str = "todo_app"
    pg_user: str = "postgres"
    pg_password: str = "postgres"
    pool_min_size: int = 1
    pool_max_size: int = 5

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            client_origin=os.getenv("CLIENT_ORIGIN", "*"),
            database_url=os.getenv("DATABASE_URL"),
            node_env=os.getenv("NODE_ENV"),
            pg_host=os.getenv("PGHOST", "localhost"),
            pg_port=int(os.getenv("PGPORT", "5432")),
            pg_database=os.getenv("PGDATABASE", "todo_app"),
            pg_user=os.getenv("PGUSER", "postgres"),
            pg_password=os.getenv("PGPASSWORD", "postgres"),
            pool_min_size=int(os.getenv("PGPOOL_MIN", "1")),
            pool_max_size=int(os.getenv("PGPOOL_MAX", "5")),
        )

    @property
    def cors_origins(self) -> List[str]:
        if self.client_origin.strip() == "*" or not self.client_origin.strip():
            return ["*"]
        return [origin.strip() for origin in self.client_origin.split(",") if origin.strip()]


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("title is required")
        return normalized


class TodoUpdate(BaseModel):
    isComplete: bool = Field(..., description="New completion state")


class Todo(BaseModel):
    id: int
    title: str
    isComplete: bool
    createdAt: datetime


def _ensure_ssl(conn_string: str, settings: Settings) -> str:
    if settings.node_env and settings.node_env.lower() == "production" and "sslmode" not in conn_string:
        separator = "&" if "?" in conn_string else "?"
        return f"{conn_string}{separator}sslmode=require"
    return conn_string


def _build_conninfo(settings: Settings) -> str:
    if settings.database_url:
        return _ensure_ssl(settings.database_url, settings)

    return conninfo.make_conninfo(
        host=settings.pg_host,
        port=settings.pg_port,
        dbname=settings.pg_database,
        user=settings.pg_user,
        password=settings.pg_password,
    )


def map_todo(row: Dict[str, Any]) -> Todo:
    created_at = row["created_at"]
    created_iso = created_at if isinstance(created_at, datetime) else datetime.fromisoformat(str(created_at))
    return Todo(
        id=row["id"],
        title=row["title"],
        isComplete=bool(row["is_complete"]),
        createdAt=created_iso,
    )


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    settings = settings or Settings.from_env()
    pool = ConnectionPool(
        conninfo=_build_conninfo(settings),
        min_size=settings.pool_min_size,
        max_size=settings.pool_max_size,
        kwargs={"row_factory": dict_row},
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            yield
        finally:
            pool.close()

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def fetch_one(query: str, params: Iterable[Any] | None = None) -> Optional[Dict[str, Any]]:
        with pool.connection() as conn, conn.cursor() as cur:
            cur.execute(query, params or [])
            return cur.fetchone()

    def fetch_all(query: str, params: Iterable[Any] | None = None) -> List[Dict[str, Any]]:
        with pool.connection() as conn, conn.cursor() as cur:
            cur.execute(query, params or [])
            return list(cur.fetchall())

    def execute(query: str, params: Iterable[Any] | None = None) -> int:
        with pool.connection() as conn, conn.cursor() as cur:
            cur.execute(query, params or [])
            conn.commit()
            return cur.rowcount

    @app.get("/api/health")
    def healthcheck() -> Dict[str, bool]:
        fetch_one("SELECT 1")
        return {"ok": True}

    @app.get("/api/todos", response_model=List[Todo])
    def list_todos() -> List[Todo]:
        rows = fetch_all(
            "SELECT id, title, is_complete, created_at FROM todos ORDER BY created_at DESC"
        )
        return [map_todo(row) for row in rows]

    @app.post("/api/todos", response_model=Todo, status_code=201)
    def create_todo(payload: TodoCreate) -> Todo:
        row = fetch_one(
            "INSERT INTO todos (title) VALUES (%s) RETURNING id, title, is_complete, created_at",
            [payload.title],
        )
        if not row:
            raise HTTPException(status_code=500, detail="Failed to create todo")
        return map_todo(row)

    @app.patch("/api/todos/{todo_id}", response_model=Todo)
    def update_todo(todo_id: int, payload: TodoUpdate) -> Todo:
        row = fetch_one(
            "UPDATE todos SET is_complete = %s WHERE id = %s RETURNING id, title, is_complete, created_at",
            [payload.isComplete, todo_id],
        )
        if not row:
            raise HTTPException(status_code=404, detail="Todo not found")
        return map_todo(row)

    @app.delete("/api/todos/{todo_id}", status_code=204, response_class=Response)
    def delete_todo(todo_id: int) -> Response:
        deleted = execute("DELETE FROM todos WHERE id = %s", [todo_id])
        if not deleted:
            raise HTTPException(status_code=404, detail="Todo not found")
        return Response(status_code=204)

    return app


app = create_app()

