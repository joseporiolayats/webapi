"""
webapi/routers/clients.py

Router for the /clients API calls
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


@router.get("name/{name}", response_description="List clients by name")
async def list_clients_by_name(
    request: Request,
    name: str = None,
) -> List[ClientDB]:
    query = {"name": name}

    full_query = request.app.mongodb["clients"].find(query).sort("_id", 1)
    return [ClientDB(**raw_customers) async for raw_customers in full_query]
