from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from .. import models
from ..database_simple import SessionLocal
from ..auth import (
    get_db,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

logger = logging.getLogger("pams.auth.routes")

router = APIRouter(prefix="/api/auth", tags=["auth"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str | None = None
    full_name: str | None = None

    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponse)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    # Check existing
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        role="user",
        hashed_password=get_password_hash(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), request: Request = None):
    logger.info("Login attempt for username=%s from %s", form.username, request.client.host if request else "unknown")
    user = authenticate_user(db, form.username, form.password)
    if not user:
        logger.warning("Login failed for username=%s", form.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user.username}, expires_delta=expires)
    logger.info("Login success username=%s", user.username)
    return TokenResponse(access_token=token, expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60)

@router.get("/me", response_model=UserResponse)
def me(current_user: models.User = Depends(get_current_user)):
    logger.debug("/me accessed by user=%s", current_user.username)
    return current_user

@router.post("/logout")
def logout():
    # Stateless JWT – client removes token
    return {"message": "Logged out. Please discard token client-side."}
