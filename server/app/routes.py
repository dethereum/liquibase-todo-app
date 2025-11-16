from __future__ import annotations

from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from .database import Database
from .schemas import Todo, TodoCreate, TodoUpdate, map_todo

api_router = APIRouter(prefix="/api")


def get_db(request: Request) -> Database:
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise RuntimeError("database not initialized")
    return db


@api_router.get("/health")
def healthcheck(db: Database = Depends(get_db)) -> Dict[str, bool]:
    db.fetch_one("SELECT 1")
    return {"ok": True}


@api_router.get("/todos", response_model=List[Todo])
def list_todos(db: Database = Depends(get_db)) -> List[Todo]:
    rows = db.fetch_all("SELECT id, title, is_complete, created_at FROM todos ORDER BY created_at DESC")
    return [map_todo(row) for row in rows]


@api_router.post("/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoCreate, db: Database = Depends(get_db)) -> Todo:
    row = db.fetch_one(
        "INSERT INTO todos (title) VALUES (%s) RETURNING id, title, is_complete, created_at",
        [payload.title],
    )
    if not row:
        raise HTTPException(status_code=500, detail="Failed to create todo")
    return map_todo(row)


@api_router.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate, db: Database = Depends(get_db)) -> Todo:
    row = db.fetch_one(
        "UPDATE todos SET is_complete = %s WHERE id = %s RETURNING id, title, is_complete, created_at",
        [payload.isComplete, todo_id],
    )
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    return map_todo(row)


@api_router.delete("/todos/{todo_id}", status_code=204, response_class=Response)
def delete_todo(todo_id: int, db: Database = Depends(get_db)) -> Response:
    deleted = db.execute("DELETE FROM todos WHERE id = %s", [todo_id])
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=204)
