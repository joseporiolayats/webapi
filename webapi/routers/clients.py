"""
webapi/routers/clients.py

This module contains the router for handling /clients API calls.
"""
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Request
from pydantic import EmailStr

from webapi.backend.classes import ClientDB
from webapi.backend.classes import Role

router = APIRouter()


@router.get("/", response_description="List clients")
async def list_clients(
    request: Request,
    name: Optional[str] = None,
    id: Optional[str] = None,
    role: Optional[Role] = None,
    email: Optional[EmailStr] = None,
) -> List[ClientDB]:
    """
    List all clients based on the given filters.

    Args:
        request (Request): FastAPI request object.
        name (Optional[str], optional): Filter clients by name. Defaults to None.
        id (Optional[str], optional): Filter clients by ID. Defaults to None.
        role (Optional[Role], optional): Filter clients by role. Defaults to None.
        email (Optional[EmailStr], optional): Filter clients by email. Defaults to None.

    Returns:
        List[ClientDB]: A list of filtered client objects.
    """
    query = {}

    if name:
        query["name"] = name
    if id:
        query["id"] = id
    if role:
        query["role"] = role
    if email:
        query["email"] = email

    full_query = request.app.mongodb["clients"].find(query).sort("_id", 1)
    return [ClientDB(**raw_customers) async for raw_customers in full_query]


@router.get("/name/{name}", response_description="List clients by name")
async def list_clients_by_name(
    request: Request,
    name: str,
) -> List[ClientDB]:
    """
    List clients with the given name.

    Args:
        request (Request): FastAPI request object.
        name (str): Name to filter clients by.

    Returns:
        List[ClientDB]: A list of client objects with the given name.
    """
    query = {"name": name}

    full_query = request.app.mongodb["clients"].find(query).sort("_id", 1)
    return [ClientDB(**raw_customers) async for raw_customers in full_query]
