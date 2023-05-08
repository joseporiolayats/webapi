"""
webapi/routers/users.py
"""
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from webapi.backend.authentication import Authorization
from webapi.backend.models import CurrentUser
from webapi.backend.models import LoginBase
from webapi.backend.models import UserBase

router = APIRouter()
auth_handler = Authorization()


@router.post("/register", response_description="Register user")
async def register(request: Request, newUser: UserBase = Body(...)) -> JSONResponse:
    """
    Register a new user in the system.

    Args:
        request (Request): FastAPI request object.
        newUser (UserBase): New user object.

    Returns:
        JSONResponse: JSON response with the created user data.
    """
    newUser.password = auth_handler.get_password_hash(newUser.password)
    newUser = jsonable_encoder(newUser)
    existing_email = await request.app.mongodb["users"].find_one(
        {"email": newUser["email"]}
    )
    if existing_email is not None:
        raise HTTPException(
            status_code=409, detail=f"User with email {newUser['email']} already exists"
        )
    existing_username = await request.app.mongodb["users"].find_one(
        {"username": newUser["username"]}
    )
    if existing_username is not None:
        raise HTTPException(
            status_code=409,
            detail=f"User with username {newUser['username']} already exists",
        )

    user = await request.app.mongodb["users"].insert_one(newUser)
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": user.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.post("/login", response_description="Login user")
async def login(request: Request, loginUser: LoginBase = Body(...)) -> JSONResponse:
    """
    Authenticate a user and return an access token.

    Args:
        request (Request): FastAPI request object.
        loginUser (LoginBase): User object with email and password.

    Returns:
        JSONResponse: JSON response containing the access token.
    """
    try:
        user = request.app.cache["clients"][loginUser.password]["email"]

        if user == loginUser.email:
            token = auth_handler.encode_token(
                request.app.cache["clients"][loginUser.password]["id"]
            )
            return JSONResponse(content={"token": token})

    except HTTPException as e:
        raise HTTPException(
            status_code=401, detail=f"Invalid email and/or password:{e}"
        ) from e


@router.get("/me", response_description="Logged in user data")
async def me(
    request: Request, userId=Depends(auth_handler.auth_wrapper)
) -> JSONResponse:
    """
    Retrieve the data of the currently logged in user.

    Args:
        request (Request): FastAPI request object.
        userId (str): User ID obtained from the authentication wrapper.

    Returns:
        JSONResponse: JSON response with the logged in user data.
    """
    currentUser = await request.app.mongodb["users"].find_one({"id": userId})
    result = CurrentUser(**currentUser).dict()
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
