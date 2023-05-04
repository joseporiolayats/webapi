"""
webapi/backend/classes.py

This script contains the classes that define the schema for the
actual data using pydantic
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    """
    Role schema in pydantic syntax
    as refered in the documentation for the problem in
    https://joseporiolayats.github.io/webapi/data
    """

    admin = "admin"
    user = "user"
    guest = "guest"


class Client(BaseModel):
    """
    Client base class schema
    as refered in the documentation for the problem in
    https://joseporiolayats.github.io/webapi/data
    """

    id: str
    name: str
    email: str
    role: Role


class Policies(BaseModel):
    """
    Policies base class schema
    as refered in the documentation for the problem in
    https://joseporiolayats.github.io/webapi/data
    """

    id: str
    amountInsured: float
    email: str
    inceptionDate: datetime
    installmentPayment: bool
    clientId: str
