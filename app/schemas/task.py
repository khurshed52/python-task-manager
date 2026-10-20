from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    completed: bool = False


class TaskUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )
    description: str | None = Field(
        default=None,
        min_length=5,
        max_length=500
    )
    completed: bool | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    completed: bool