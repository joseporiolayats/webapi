"""
webapi/backend/authentication.py
"""
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

SECRET_KEY = config("SECRET_KEY", cast=str)


class Authorization:
    """
    Class to handle user authorization and token generation.
    """

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, secret: str = SECRET_KEY):
        self.secret = secret

    def get_password_hash(self, password: str) -> str:
        """
        Hash the given password.

        Args:
            password (str): Password to be hashed.

        Returns:
            str: Hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify if the plain password matches the hashed password.

        Args:
            plain_password (str): Plain password to be verified.
            hashed_password (str): Hashed password to be compared.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        """
        Encode the token for the given user ID.

        Args:
            user_id (str): User ID to be encoded in the token.

        Returns:
            str: Encoded token.
        """
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=0, minutes=35),
            "iat": datetime.now(timezone.utc),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        """
        Decode the token and return the user ID.

        Args:
            token (str): Token to be decoded.

        Returns:
            str: User ID from the decoded token.

        Raises:
            HTTPException: If the token is expired or invalid.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Signature has expired") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token") from e

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """
        Wrapper function for the token decoding process.

        Args:
            auth (HTTPAuthorizationCredentials, optional):
            FastAPI HTTPAuthorizationCredentials object.

        Returns:
            str: User ID from the decoded token.
        """

        return self.decode_token(auth.credentials)
