"""Runtime configuration helpers for the FastAPI app."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Container for database and server configuration."""

    pg_user: str
    pg_password: str
    client_origin: str = '*'
    database_url: str | None = None
    node_env: str | None = None
    pg_host: str = 'localhost'
    pg_port: int = 5432
    pg_database: str = 'todo_app'
    pool_min_size: int = 1
    pool_max_size: int = 5

    @classmethod
    def from_env(cls) -> Settings:
        """Build a Settings instance from environment variables."""
        pg_user = os.getenv('PGUSER')
        pg_password = os.getenv('PGPASSWORD')
        missing = [
            name
            for name, value in (
                ('PGUSER', pg_user),
                ('PGPASSWORD', pg_password),
            )
            if not value
        ]
        if missing:
            missing_vars = ', '.join(missing)
            raise RuntimeError(
                f'Missing required environment variable(s): {missing_vars}'
            )

        return cls(
            pg_user=pg_user,
            pg_password=pg_password,
            client_origin=os.getenv('CLIENT_ORIGIN', '*'),
            database_url=os.getenv('DATABASE_URL'),
            node_env=os.getenv('NODE_ENV'),
            pg_host=os.getenv('PGHOST', 'localhost'),
            pg_port=int(os.getenv('PGPORT', '5432')),
            pg_database=os.getenv('PGDATABASE', 'todo_app'),
            pool_min_size=int(os.getenv('PGPOOL_MIN', '1')),
            pool_max_size=int(os.getenv('PGPOOL_MAX', '5')),
        )

    @property
    def cors_origins(self) -> list[str]:
        """Return parsed CORS origins honoring '*' as allow-all."""
        if self.client_origin.strip() == '*' or not self.client_origin.strip():
            return ['*']
        return [
            origin.strip()
            for origin in self.client_origin.split(',')
            if origin.strip()
        ]
