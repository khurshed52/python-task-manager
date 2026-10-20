from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_all_tasks(db: Session):
    statement = select(Task).order_by(Task.id)

    return db.scalars(statement).all()


def get_task_by_id(db: Session, task_id: int):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


def create_task(db: Session, data: TaskCreate):
    new_task = Task(
        name=data.name,
        description=data.description,
        completed=data.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def update_task(db: Session, task_id: int, data: TaskUpdate):
    task = get_task_by_id(db, task_id)

    update_data = data.model_dump(exclude_unset=True)

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=422,
            detail="Task fields cannot be null"
        )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}