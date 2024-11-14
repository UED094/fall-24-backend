from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.services.user as user_service
from app.core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    decode_access_token,
    oauth2_scheme,
)
from app.dependencies import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from fastapi import status

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = user_service.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # if not user.is_verified:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Email not verified",
    #     )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    decoded_token = decode_access_token(token)
    if decoded_token is None or decoded_token.username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    username = decoded_token.username
    user = user_service.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/verify-email/{verification_code}")
def verify_email(verification_code: str, db: Session = Depends(get_db)):
    return user_service.verify_email(verification_code, db)
