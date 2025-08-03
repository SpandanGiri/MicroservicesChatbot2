from pydantic import BaseModel


class User(BaseModel):
    username : str
    email : str | None = None
    disabled : bool


class UserInDB(User):
    hashed_password: str

class UserLogin(BaseModel):
    username: str
    password: str
    email : str | None = None