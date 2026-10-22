from fastapi import FastAPI

from app.routers.tasks import router as task_router
from app.routers.auth import router as auth_router


app = FastAPI(
    title="Task Manager API",
    version="1.0.0"
)

app.include_router(task_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}