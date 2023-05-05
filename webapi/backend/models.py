"""
webapi/backend/models.py
"""
from email_validator import EmailNotValidError
from email_validator import validate_email
from pydantic import EmailStr
from pydantic import Field
from pydantic import validator

from webapi.backend.classes import BaseModel
from webapi.backend.classes import MongoBaseModel
from webapi.backend.classes import Role


class UserBase(MongoBaseModel):
    username: str = Field(..., min_length=3, max_length=15)
    email: str = EmailStr(...)
    password: str = Field(...)
    role: Role

    @validator("email")
    def valid_email(cls, v):
        try:
            email = validate_email(v).email
            return email
        except EmailNotValidError as e:
            raise EmailNotValidError from e


class LoginBase(BaseModel):
    email: str = EmailStr(...)
    password: str = Field(...)


class CurrentUser(BaseModel):
    email: str = EmailStr(...)
    username: str = Field(...)
    role: str = Field(...)
