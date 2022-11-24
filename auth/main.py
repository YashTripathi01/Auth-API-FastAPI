from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from auth import models, crud, schemas, database, utils

app = FastAPI(title='User Authentication Routes')

models.Base.metadata.create_all(bind=database.engine)


@app.get('/')
def root():
    return {'msg': 'MP4 to MP3 Microservice Architecture Implementation.'}


@app.get('/users', response_model=List[schemas.UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users_list = crud.get_users(db=db, skip=skip, limit=limit)

    return users_list


@app.get('/users/{id}', response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    user = crud.get_user(db=db, user_id=id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    return user


@app.post('/register', response_model=schemas.UserResponse)
def register(request: schemas.RegisterUser, db: Session = Depends(database.get_db)):
    user_exists = crud.get_user_by_email(db=db, email=request.email)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered.')

    return crud.register_user(db=db, request=request)


@app.post('/login', response_model=schemas.Token)
def login(request: schemas.LoginUser, db: Session = Depends(database.get_db)):
    user_exists = crud.get_user_by_email(db=db, email=request.email)

    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Credentials.')

    return crud.login_user(db=db, request=request, existing_user=user_exists)


@app.post('/validate', response_model=schemas.UserResponse)
def validate_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Bearer'})

    return utils.verify_access_token(token=token, exception=credentials_exception)
