from pydantic import BaseModel, EmailStr


class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
