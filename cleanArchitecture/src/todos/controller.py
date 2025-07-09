from fastapi import APIRouter, status
from typing import List
from uuid import UUID
from ..database.core import DbSession
from . import service
from . import model
from ..auth.service import CurrentUser
from src.entities.todo import Todo

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.post("/", response_model=model.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(db:DbSession, todo:model.TodoCreate, current_user:CurrentUser):
    return service.create_todo(current_user, db, todo)

@router.get("/", response_model=List[Todo])
def get_todos(db:DbSession, current_user:CurrentUser):
    return service.get_todos(current_user, db)

@router.get("/{todo_id}", response_model=Todo)
def get_todo(db:DbSession, todo_id:UUID, current_user:CurrentUser):
    return service.get_todo_by_id(current_user, db, todo_id)

@router.put("/{todo_id}", response_model=Todo)
def update_todo(db:DbSession, todo_id:UUID, current_user:CurrentUser, todo_update:model.TodoCreate):
    return service.update_todo(current_user, db, todo_id, todo_update)

@router.put("/{todo_id}/complete", response_model=model.TodoResponse)
def complete_todo(db:DbSession, todo_id:UUID, current_user:CurrentUser):
    return service.complete_todo(current_user, db, todo_id)


@router.delete("/{todo_id}", response_model=model.TodoResponse)
def delete_todo(db:DbSession, todo_id:UUID, current_user:CurrentUser):
    return service.delete_todo(current_user, db, todo_id)
