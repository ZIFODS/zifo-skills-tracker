from pydantic import BaseModel


class ConsultantBase(BaseModel):
    name: str
    email: str


class ConsultantCreate(ConsultantBase):
    pass


class Consultant(ConsultantBase):
    type: str


class ConsultantList(BaseModel):
    items: list[Consultant]
