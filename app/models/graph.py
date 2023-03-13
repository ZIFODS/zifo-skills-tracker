from typing import Optional

from pydantic import BaseModel


class Rule(BaseModel):
    """
    Element in the skill search rule list.
    Name corresponds to name of skill.
    Operator is AND/OR that applies to skill or parenthesis before.
    Parenthesis determines if the skill is at the start or end of a parenthesis.
    """
    name: str
    operator: str
    parenthesis: str


class Link(BaseModel):
    """
    Relationship in the graph between a source node ID and a target node ID.
    """
    id: int
    source: int
    target: int


class Node(BaseModel):
    """
    Node returned from the graph.
    Can be a consultant or a skill.
    Skills have an category and consultants have an email.
    """
    id: int
    name: str
    type: str
    category: Optional[str]
    email: Optional[str]


class GraphData(BaseModel):
    """
    Nodes and relationships that form a graph structure.
    """
    nodes: list[Node]
    links: list[Link]
