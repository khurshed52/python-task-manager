from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


def get_owned_task(
    db: Session,
    task_id: int,
    current_user: User
) -> Task:
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


def get_all_tasks(db: Session, current_user: User):
    statement = select(Task).where(
        Task.user_id == current_user.id
    )

    return db.scalars(statement).all()


def get_task_by_id(
    db: Session,
    task_id: int,
    current_user: User
):
    return get_owned_task(db, task_id, current_user)

def create_task(
    db: Session,
    data: TaskCreate,
    current_user: User
):
    new_task = Task(
        **data.model_dump(),
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def update_task(
    db: Session,
    task_id: int,
    data: TaskUpdate,
    current_user: User
):
    task = get_owned_task(db, task_id, current_user)

    for field, value in data.model_dump(
        exclude_unset=True
    ).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task

def delete_task(
    db: Session,
    task_id: int,
    current_user: User
):
    task = get_owned_task(db, task_id, current_user)

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}