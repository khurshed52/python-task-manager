from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import tasks as task_service


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: DbSession):
    return task_service.get_all_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: DbSession):
    return task_service.get_task_by_id(db, task_id)


@router.post("/", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate, db: DbSession):
    return task_service.create_task(db, task)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: DbSession
):
    return task_service.update_task(db, task_id, task_update)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: DbSession):
    return task_service.delete_task(db, task_id)