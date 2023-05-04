"""
webapi/backend/classes.py

This script contains the classes that define the schema for the
actual data using pydantic
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # id: PyObjectId = Field(default_factory=PyObjectId)

    class Config:
        json_encoders = {ObjectId: str}


class Role(str, Enum):
    """
    Role schema in pydantic syntax
    as referred in the documentation for the problem in
    https://joseporiolayats.github.io/webapi/data
    """

    admin = "admin"
    user = "user"
    guest = "guest"


class ClientBase(MongoBaseModel):
    """
    Client base class schema
    as referred in the documentation for the problem in
    https://joseporiolayats.github.io/webapi/data
    """

    id: str = Field(...)
    name: str = Field(..., min_length=3)
    email: str = Field(..., min_length=6)
    role: Role = Field(...)


class ClientUpdate(MongoBaseModel):
    """
    Class for updating some values of a client
    """

    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None


class ClientDB(ClientBase):
    """
    Class to follow convention of having a model that represent the instance
    of the database.
    """

    pass


class PoliciesBase(MongoBaseModel):
    """
    Policies base class schema
    as referred in the documentation for the problem in
    https://joseporiolayats.github.io/webapi/data
    """

    id: str = Field(...)
    amountInsured: float = Field(...)
    email: str = Field(..., min_length=6)
    inceptionDate: datetime = Field(...)
    installmentPayment: bool = Field(...)
    clientId: str = Field(...)


class PoliciesUpdate(MongoBaseModel):
    """
    Class for updating some values of the policies associated with a client
    """

    amountInsured: Optional[float] = None
    email: Optional[str] = None
    installmentPayment: Optional[bool] = None


class PoliciesDB(PoliciesBase):
    """
    Class to follow convention of having a model that represent the instance
    of the database.
    """

    pass
