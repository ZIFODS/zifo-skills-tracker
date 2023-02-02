from pydantic import BaseModel

class Node(BaseModel):
    id: int
    name: str
    group: str

class Link(BaseModel):
    id: int
    source: int
    target: int

class GraphData(BaseModel):
    nodes: list[Node]
    links: list[Link]