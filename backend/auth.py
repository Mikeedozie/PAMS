from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database_simple import SessionLocal
from . import models

import os, logging

logger = logging.getLogger("pams.auth")
logging.basicConfig(level=logging.INFO)

SECRET_KEY = os.getenv("PAMS_SECRET_KEY", "CHANGE_ME_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 6  # 6 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": now})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("Created access token for sub=%s exp=%s", data.get("sub"), expire.isoformat())
    return token

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username)
    if not user:
        logger.warning("Auth failed: user '%s' not found", username)
        return None
    if not verify_password(password, user.hashed_password or ""):
        logger.warning("Auth failed: bad password for user '%s'", username)
        return None
    logger.info("Auth success for user '%s'", username)
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            logger.warning("Token decode failed: missing sub")
            raise credentials_exception
    except JWTError as e:
        logger.warning("Token decode error: %s", e)
        raise credentials_exception
    user = get_user_by_username(db, username=username)
    if user is None:
        logger.warning("Token user not found: %s", username)
        raise credentials_exception
    return user
