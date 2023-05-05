"""
webapi/backend/authentication.py
"""
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt
from fastapi import HTTPException
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from passlib.context import CryptContext


class Authorization:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = "SuperSecretString"

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=0, minutes=35),
            "iat": datetime.now(timezone.utc),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Signature has expired") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token") from e

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
