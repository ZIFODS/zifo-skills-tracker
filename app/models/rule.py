from pydantic import BaseModel

class Rule(BaseModel):
    name: str
    group: str
    operator: str
    parenthesis: str