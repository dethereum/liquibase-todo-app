"""Lightweight database helper built on psycopg connection pools."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from psycopg import conninfo
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from .settings import Settings


def _ensure_ssl(conn_string: str, settings: Settings) -> str:
    if (
        settings.node_env
        and settings.node_env.lower() == 'production'
        and 'sslmode' not in conn_string
    ):
        separator = '&' if '?' in conn_string else '?'
        return f'{conn_string}{separator}sslmode=require'
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


class Database:
    """Wraps a psycopg connection pool with small helper methods."""

    def __init__(self, settings: Settings):
        """Initialize using DATABASE_URL or discrete settings."""
        self._pool = ConnectionPool(
            conninfo=_build_conninfo(settings),
            min_size=settings.pool_min_size,
            max_size=settings.pool_max_size,
            kwargs={'row_factory': dict_row},
        )

    def close(self) -> None:
        """Close the underlying pool and release all open connections."""
        self._pool.close()

    def fetch_one(
        self, query: str, params: Iterable[Any] | None = None
    ) -> dict[str, Any] | None:
        """Run a SELECT and return a single row as a dict, if available."""
        with self._pool.connection() as conn, conn.cursor() as cur:
            cur.execute(query, params or [])
            return cur.fetchone()

    def fetch_all(
        self, query: str, params: Iterable[Any] | None = None
    ) -> list[dict[str, Any]]:
        """Run a SELECT and return every row as dictionaries."""
        with self._pool.connection() as conn, conn.cursor() as cur:
            cur.execute(query, params or [])
            return list(cur.fetchall())

    def execute(self, query: str, params: Iterable[Any] | None = None) -> int:
        """Execute a mutating statement and return affected row count."""
        with self._pool.connection() as conn, conn.cursor() as cur:
            cur.execute(query, params or [])
            conn.commit()
            return cur.rowcount
