from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import tasks as task_service
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.tasks import (create_task, get_all_tasks, get_task_by_id, update_task, delete_task)
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)]
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[TaskResponse])
def get_tasks_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_tasks(db, current_user)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_task_by_id(db, task_id, current_user)


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task_route(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task(db, data, current_user)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_route(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_task(db, task_id, data, current_user)


@router.delete("/{task_id}")
def delete_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_task(db, task_id, current_user)