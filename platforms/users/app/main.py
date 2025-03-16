from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status
from starlette.exceptions import HTTPException

app = FastAPI()

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


class User(BaseModel):
    id: str
    first_name: str
    last_name: str

    @staticmethod
    def from_db(user_data: dict) -> "User":
        return User(**user_data)





@app.get("/users")
def get_users() -> list[User]:
    return [User.from_db(user_data) for user_data in USERS_BY_ID.values()]


@app.get("/users/{user_id}")
def get_user(user_id: str) -> User:
    user_data = USERS_BY_ID.get(user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return User.from_db(user_data)


# @app.get("/login")
# def login(username: str, password: str) -> dict:
#     users = [user for user in USERS_BY_ID.values() if user["username"] == username]
#     if len(users) == 0 or len(users) > 1:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     user_data = users[0]
#     if user_data["password"] != password:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     return py
