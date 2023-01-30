from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        orm_mode = True


class UserAuth(User):
    password: str
