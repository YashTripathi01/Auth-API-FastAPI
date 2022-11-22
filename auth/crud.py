from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from . import models, schemas, utils


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def register_user(db: Session, request: schemas.RegisterUser):
    new_password = utils.hash(request.password)
    request.password = new_password

    user = models.User(**request.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, request: schemas.LoginUser):
    user_exists = get_user_by_email(db=db, email=request.email)

    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Credentials.')

    verify_password = utils.verify_hash(
        hashed_password=user_exists.password, plain_password=request.password)

    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Credentials.')

    return {'msg': 'Login successful'}
