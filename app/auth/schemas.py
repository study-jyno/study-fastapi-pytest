from typing import Optional, List, Dict, Any

from pydantic import BaseModel

from datetime import datetime


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    is_admin: Optional[bool] = False


class CreateUser(User):
    password: str


class UpdateUser(User):
    user_id: int
    password: Optional[str]


class ShowUser(User):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    username: str
    new_password: str
    check_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class BaseUserCertification(BaseModel):
    user_id: int
    certification_string: str


class RequestUserCertification(BaseModel):
    username: str


class ConfirmUserCertification(BaseModel):
    username: str
    certification_string: str


class CreateUserCertification(BaseUserCertification):
    pass


class UpdateUserCertification(BaseUserCertification):
    pass


class ShowUserCertification(BaseUserCertification):
    created_time: datetime
