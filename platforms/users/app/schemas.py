import uuid
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str

    @staticmethod
    def from_db(user_data: dict) -> "User":
        return User(**user_data)


class JWTClaims(BaseModel):
    # standard claims
    iss: str = "sofos"
    sub: str
    aud: Union[str, list[str]] = "sofos"
    exp: int
    nbf: int
    iat: int
    jti: str = Field(default_factory=uuid.uuid4)
    # custom claims
    username: str


class LoginResponse(BaseModel):
    token: str
    type: str = "bearer"
