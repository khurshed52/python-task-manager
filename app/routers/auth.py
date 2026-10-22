from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserRegister, UserResponse, UserLogin, TokenResponse
from app.services.auth import register_user, authenticate_user
from app.core.jwt import create_access_token
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/register",
    status_code=201,
    response_model=UserResponse
)
def register(data: UserRegister, db: DbSession):
    return register_user(db, data)

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: DbSession):
    user = authenticate_user(db, data)

    access_token = create_access_token(str(user.id))

    return TokenResponse(
        access_token=access_token
    )

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user