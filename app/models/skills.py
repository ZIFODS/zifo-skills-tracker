from pydantic import BaseModel


class Skill(BaseModel):
    name: str
    section: str


class SkillList(BaseModel):
    skills: list[Skill]
