from app.database import SessionLocal
from app.models.task import Task

with SessionLocal() as db:
    task = Task(
        name="Test Transaction",
        description="Learning database rollback",
        completed=False
    )

    db.add(task)

    db.flush()

    print("Task ID:", task.id)

    db.rollback()

    print("Transaction rolled back")