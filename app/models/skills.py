from pydantic import BaseModel


class SkillBase(BaseModel):
    name: str
    category: str


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    type: str


class SkillList(BaseModel):
    items: list[Skill]


class CategoryList(BaseModel):
    items: list[str]
