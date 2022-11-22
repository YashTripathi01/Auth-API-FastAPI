from werkzeug.security import generate_password_hash, check_password_hash


def hash(password: str):
    return generate_password_hash(password)


def verify_hash(hashed_password: str, plain_password: str):
    return check_password_hash(hashed_password, plain_password)
