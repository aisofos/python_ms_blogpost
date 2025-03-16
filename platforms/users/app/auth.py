import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from pydantic import ValidationError
from app.schemas import User
from app.schemas import JWTClaims

# Secret key for JWT signing - in production, use a secure environment variable
SECRET_KEY = "your-secret-key-here"  # Change this in production
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24


def get_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    claims = JWTClaims(
        sub=str(user.id),
        exp=int((now + timedelta(minutes=TOKEN_EXPIRE_MINUTES)).timestamp()),
        nbf=int(now.timestamp()),
        iat=int(now.timestamp()),
        jti=str(uuid.uuid4()),
        username=user.username,
    )
    return jwt.encode(
        claims.model_dump(exclude_none=True), SECRET_KEY, algorithm=ALGORITHM
    )


def decode_token(token: str) -> JWTClaims:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": True},
        )
        claims = JWTClaims(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return claims
