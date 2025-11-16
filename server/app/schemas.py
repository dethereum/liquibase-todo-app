from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field, field_validator


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


def map_todo(row: Dict[str, Any]) -> Todo:
    created_at = row["created_at"]
    created_iso = created_at if isinstance(created_at, datetime) else datetime.fromisoformat(str(created_at))
    return Todo(
        id=row["id"],
        title=row["title"],
        isComplete=bool(row["is_complete"]),
        createdAt=created_iso,
    )
