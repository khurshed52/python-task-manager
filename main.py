from fastapi import FastAPI

from app.routers.tasks import router as task_router


app = FastAPI(
    title="Task Manager API",
    description="My first FastAPI CRUD project",
    version="1.0.0"
)

app.include_router(task_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Task Manager API"
    }