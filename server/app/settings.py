from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional


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
