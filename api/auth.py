from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import utils
from database import get_db_session
from models import User
from schemas.token import TokenResponseSchema
from schemas.users import RegisterUserSchema
from utils import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_password_hash

auth_router = APIRouter(prefix="", tags=['Authentication'])


@auth_router.post('/register')
def register(user_data: RegisterUserSchema):
    hashed_password = get_password_hash(user_data.password)

    with get_db_session() as db_session:
        existing_user = db_session.query(User).filter_by(user_name=user_data.username).first()

        if existing_user:
            return {
                "massage": "email or user_name already exist",
                "status": "Not registered"
            }

        user = User(user_name=user_data.username, email=user_data.email, hash_password=hashed_password)

        db_session.add(user)
        db_session.commit()
        return {
            "massage": "Well come",
            "status": "Registration done successfully"
        }


@auth_router.post('/login', response_model=TokenResponseSchema)
def login(user_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = authenticate_user(user_data.username, user_data.password)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_data.username}, expires_delta=access_token_expires)
    return {
            "access_token": access_token,
            "token_type": "bearer"
            }


@auth_router.delete('/remove_user', description="authentication required for remove user!")
def delete_user(user_id: str, current_user: User = Depends(utils.get_current_user)):
    with get_db_session() as db_session:
        user: User = db_session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Store '{user_id}' cannot be found.",
            )
        db_session.delete(user)
        db_session.commit()

        return user.user_name + " has been deleted"
