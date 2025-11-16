"""Pydantic models and helpers for todo payloads."""

from __future__ import annotations

import datetime as dt
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TodoCreate(BaseModel):
    """Incoming payload body when creating a todo."""

    title: str = Field(..., min_length=1, max_length=255)

    @field_validator('title')
    @classmethod
    def normalize_title(cls, value: str) -> str:
        """Trim whitespace and ensure the title is non-empty."""
        normalized = value.strip()
        if not normalized:
            raise ValueError('title is required')
        return normalized


class TodoUpdate(BaseModel):
    """Payload for toggling completion state on an existing todo."""

    model_config = ConfigDict(populate_by_name=True)

    is_complete: bool = Field(
        ...,
        description='New completion state',
        validation_alias='isComplete',
        serialization_alias='isComplete',
    )


class Todo(BaseModel):
    """Full representation of a todo returned by the API."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    title: str
    is_complete: bool = Field(
        ...,
        validation_alias='isComplete',
        serialization_alias='isComplete',
    )
    created_at: dt.datetime = Field(
        ...,
        validation_alias='createdAt',
        serialization_alias='createdAt',
    )


def map_todo(row: dict[str, Any]) -> Todo:
    """Convert a database row into the API schema."""
    created_at = row['created_at']
    created_iso = (
        created_at
        if isinstance(created_at, dt.datetime)
        else dt.datetime.fromisoformat(str(created_at))
    )
    return Todo(
        id=row['id'],
        title=row['title'],
        is_complete=bool(row['is_complete']),
        created_at=created_iso,
    )
