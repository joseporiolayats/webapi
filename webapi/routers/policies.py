"""
webapi/routers/policies.py

Router for the /policies API calls
"""
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

from fastapi import APIRouter
from fastapi import Request
from pydantic import EmailStr

from webapi.backend.classes import ClientDB
from webapi.backend.classes import PoliciesDB

router = APIRouter()


@router.get("/", response_description="List policies")
async def list_policies(
    request: Request,
    amountInsured: Optional[float] = None,
    id: Optional[str] = None,
    clientId: Optional[str] = None,
    inceptionDate: Optional[datetime] = None,
    installmentPayment: Optional[bool] = None,
    email: Optional[EmailStr] = None,
) -> List[PoliciesDB]:
    query = {}

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

    full_query = request.app.mongodb["policies"].find(query).sort("_id", 1)
    return [PoliciesDB(**raw_customers) async for raw_customers in full_query]


@router.get(
    "/by_client_name/{client_name}", response_description="List policies by client name"
)
async def list_policies_by_client_name(
    request: Request, client_name: str
) -> Union[List[PoliciesDB], None]:
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
    request: Request, policy_id: str
) -> Union[List[ClientDB], None]:
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
    print(result)
    if result:
        return [
            ClientDB(**client)
            for policy in result
            for client in policy.get("client_info", [])
        ]
    else:
        return None


@router.get(
    "/by_policy/{policy_id}/{datafield}",
    response_description="List client datafield from policy",
)
async def list_client_by_policy_with_datafield(
    request: Request, policy_id: str, datafield: str
) -> Union[List[ClientDB] | str | dict, None]:
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
        answer = [
            ClientDB(**client)
            for policy in result
            for client in policy.get("client_info", [])
        ]

        return dict(answer[0])[datafield]
    else:
        return None
