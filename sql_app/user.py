from typing import Optional

from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256
from jose import JWSError, jwt
from datetime import datetime, timedelta
from .database import Session
from .models import User
from . import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_pass(password: str, password_hash: str):
    return pbkdf2_sha256.verify(password, password_hash)


def get_pass_hash(password: str):
    return pbkdf2_sha256.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_all_user(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: schemas.UserCreate):
    pass_hash = get_pass_hash(user.password)
    new_user = User(username=user.username, password=pass_hash, email=user.email)
    db.add(new_user)
    db.commit()
    return new_user


def check_user_exist(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt