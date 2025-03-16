from typing import Any, Dict

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import decode
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request

from app.auth import decode_token


class GetAuthenticationCredentials:
    async def __call__(
        self,
        request: Request,
        auth_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> str:
        if not auth_credentials:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return auth_credentials.credentials


class AuthRequired:
    async def __call__(
        self,
        request: Request,
        token: str = Depends(GetAuthenticationCredentials()),
    ) -> Dict[str, Any]:
        try:
            claims = decode_token(token)
            request.state.claims = claims
        except (
            ValidationError,
            ExpiredSignatureError,
            InvalidSignatureError,
            InvalidTokenError,
        ) as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from exc
        return claims