from pydantic import BaseModel


class Skill(BaseModel):
    name: str
    category: str


class SkillList(BaseModel):
    skills: list[Skill]
