from typing import Optional

from pydantic import BaseModel


class Rule(BaseModel):
    name: str
    operator: str
    parenthesis: str


class Link(BaseModel):
    id: int
    source: int
    target: int


class Node(BaseModel):
    id: int
    name: str
    type: str
    category: Optional[str]
    email: Optional[str]


class GraphData(BaseModel):
    nodes: list[Node]
    links: list[Link]
