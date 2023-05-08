"""
webapi/routers/policies.py

This module contains the router for handling /policies API calls.
"""
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from pydantic import EmailStr

from webapi.backend.authentication import Authorization
from webapi.backend.classes import ClientDB
from webapi.backend.classes import PoliciesDB

router = APIRouter()
auth_handler = Authorization()


@router.get("/", response_description="List policies")
async def list_policies(
    request: Request,
    amountInsured: Optional[float] = None,
    id: Optional[str] = None,
    clientId: Optional[str] = None,
    inceptionDate: Optional[datetime] = None,
    installmentPayment: Optional[bool] = None,
    email: Optional[EmailStr] = None,
    userId: str = Depends(auth_handler.auth_wrapper),
) -> List[PoliciesDB]:
    """
    List all policies based on the given filters.

    Args:
        request (Request): FastAPI request object.
        amountInsured (Optional[float], optional): Filter policies by amount insured.
        Defaults to None.
        id (Optional[str], optional): Filter policies by ID.
        Defaults to None.
        clientId (Optional[str], optional): Filter policies by client ID.
        Defaults to None.
        inceptionDate (Optional[datetime], optional): Filter policies by inception date.
        Defaults to None.
        installmentPayment (Optional[bool], optional): Filter policies by
        installment payment.
        Defaults to None.
        email (Optional[EmailStr], optional): Filter policies by email.
        Defaults to None.
        userId (str, optional): User ID from the authorization wrapper.

    Returns:
        List[PoliciesDB]: A list of filtered policy objects.
    """
    user = await request.app.mongodb["clients"].find_one({"id": userId})
    print(user)
    if user is None or user["role"] != "admin":
        raise HTTPException(status_code=401, detail="Content restricted to admins")

    query = {"id": userId}
    #
    if amountInsured:
        query["amountInsured"] = amountInsured
    if inceptionDate:
        query["inceptionDate"] = inceptionDate
    if id:
        query["id"] = id
    if clientId:
        query["clientId"] = clientId
    if email:
        query["email"] = email
    if installmentPayment:
        query["installmentPayment"] = installmentPayment
    print(f"Query is {query}")
    full_query = request.app.mongodb["policies"].find(query).sort("_id", 1)
    return [PoliciesDB(**raw_customers) async for raw_customers in full_query]


@router.get(
    "/by_client_name/{client_name}", response_description="List policies by client name"
)
async def list_policies_by_client_name(
    request: Request, client_name: str, userId: str = Depends(auth_handler.auth_wrapper)
) -> Union[List[PoliciesDB], None]:
    """
    List policies by the given client name.

    Args:
        request (Request): FastAPI request object.
        client_name (str): Client name to filter policies by.
        userId (str, optional): User ID from the authorization wrapper.

    Returns:
        Union[List[PoliciesDB], None]: A list of policy objects with the
        given client name or None if not found.
    """

    # Authentication
    user = await request.app.mongodb["clients"].find_one({"id": userId})
    if user is None or user["role"] != "admin":
        raise HTTPException(status_code=401, detail="Content restricted to admins")

    pipeline = [
        {"$match": {"name": client_name}},
        {
            "$lookup": {
                "from": "policies",
                "localField": "id",
                "foreignField": "clientId",
                "as": "policies_info",
            }
        },
    ]

    result = await request.app.mongodb["clients"].aggregate(pipeline).to_list(None)

    if result:
        return [
            PoliciesDB(**policy)
            for client in result
            for policy in client.get("policies_info", [])
        ]
    else:
        return None


@router.get("/by_policy/{policy_id}", response_description="List client from policy")
async def list_client_by_policy(
    request: Request, policy_id: str, userId: str = Depends(auth_handler.auth_wrapper)
) -> Union[List[ClientDB], None]:
    """
    List the client associated with the given policy ID.
    Args:
    request (Request): FastAPI request object.
    policy_id (str): Policy ID to find the associated client.
    userId (str, optional): User ID from the authorization wrapper.

    Returns:
        Union[List[ClientDB], None]: A list of client objects
         associated with the policy or None if not found.
    """

    # Authentication
    user = await request.app.mongodb["clients"].find_one({"id": userId})
    if user is None or user["role"] != "admin":
        raise HTTPException(status_code=401, detail="Content restricted to admins")

    pipeline = [
        {"$match": {"id": policy_id}},
        {
            "$lookup": {
                "from": "clients",
                "localField": "clientId",
                "foreignField": "id",
                "as": "client_info",
            }
        },
    ]
    result = await request.app.mongodb["policies"].aggregate(pipeline).to_list(None)

    if result:
        return [
            ClientDB(**client)
            for policy in result
            for client in policy.get("client_info", [])
        ]
    else:
        return None
