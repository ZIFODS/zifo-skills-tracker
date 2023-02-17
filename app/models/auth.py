import datetime

from pydantic import BaseModel


class InternalAuthToken(BaseModel):
    code: str


class ExternalAuthToken(BaseModel):
    code: str


class InternalAccessTokenData(BaseModel):
    sub: str


class ExternalUser(BaseModel):
    email: str
    username: str
    external_sub_id: str


class InternalUser(BaseModel):
    external_sub_id: str
    internal_sub_id: str
    username: str
    created_at: datetime.datetime
