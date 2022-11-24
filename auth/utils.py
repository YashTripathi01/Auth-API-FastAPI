from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from jose import jwt, JWTError
from decouple import config


def hash(password: str):
    return generate_password_hash(password)


def verify_hash(hashed_password: str, plain_password: str):
    return check_password_hash(hashed_password, plain_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + \
        timedelta(minutes=config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=float))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,
                             config('SECRET_KEY', cast=str),
                             algorithm=config('ALGORITHM', cast=str))
    return encoded_jwt


def verify_access_token(token: str, exception: Exception):
    try:
        payload = jwt.decode(token, config('SECRET_KEY', cast=str), algorithms=[
                             config('ALGORITHM', cast=str)])

        return payload
    except JWTError:
        raise exception
