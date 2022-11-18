from pydantic import BaseModel

class Nodes(BaseModel):
    id: int
    name: str
    group: str

class Links(BaseModel):
    id: int
    source: int
    target: int

class GraphData(BaseModel):
    nodes: Nodes
    links: Links