from fastapi import Depends
from fastapi import FastAPI

from webapi.backend.authentication import Authorization

app = FastAPI()
authorization = Authorization()


@app.get("/gateway")
async def gateway(user_id: str = Depends(authorization.auth_wrapper)):
    # Your logic to return more information to admin users
    return {"message": "Welcome, user! Here's the information you can access."}
