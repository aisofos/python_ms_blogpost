from fastapi import FastAPI, Depends
from starlette import status
from starlette.exceptions import HTTPException

from app.auth import get_token
from app.dependencies import AuthRequired
from app.schemas import User, LoginResponse, JWTClaims

app = FastAPI()

"""
You should never store non hashed passwords, use bcrypt, argon or equivalent.
Skipping for simplicity
"""
USERS_BY_ID = {
    "1": {
        "id": "1",
        "username": "jdoe",
        "first_name": "John",
        "last_name": "Doe",
        "password": "pass",
    },
    "2": {
        "id": "2",
        "username": "jadoe",
        "first_name": "Jane",
        "last_name": "Doe",
        "password": "pass",
    },
    "3": {
        "id": "3",
        "username": "js",
        "first_name": "John",
        "last_name": "Smith",
        "password": "pass",
    },
    "4": {
        "id": "4",
        "username": "jas",
        "first_name": "Jane",
        "last_name": "Smith",
        "password": "pass",
    },
    "5": {
        "id": "5",
        "username": "jj",
        "first_name": "John",
        "last_name": "Jones",
        "password": "pass",
    },
    "6": {
        "id": "6",
        "username": "jaj",
        "first_name": "Jane",
        "last_name": "Jones",
        "password": "pass",
    },
}


@app.get("/users/me")
def get_user(claims: JWTClaims = Depends(AuthRequired())) -> User:
    user_data = USERS_BY_ID.get(claims.sub)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return User.from_db(user_data)


@app.get("/login")
def login(username: str, password: str) -> LoginResponse:
    users = [user for user in USERS_BY_ID.values() if user["username"] == username]
    if len(users) == 0 or len(users) > 1 or not password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_data = users[0]
    if user_data["password"] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return LoginResponse(token=get_token(User.from_db(user_data)))
