import datetime

from pydantic import BaseModel


class ExternalToken(BaseModel):
    access_token: str
    expires_in: int


class ExternalUser(BaseModel):
    id: str
    email: str
    username: str


class InternalUser(BaseModel):
    external_id: str
    internal_id: str
    username: str
    created_at: datetime.datetime
