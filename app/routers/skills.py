from typing import Any

from fastapi import APIRouter

from app.schemas.skills import SkillList
from app.utils.skills import pull_skills_schema_from_s3

skills_router = APIRouter()


@skills_router.get("/", response_model=SkillList)
async def list_all_skills() -> Any:
    """
    Returns a list of all skills in the current skills schema.

    Returns
    -------
    SkillList
    """
    schema_df = pull_skills_schema_from_s3()
    schema_dict = schema_df.astype(str).to_dict(orient="list")
    schema_dict = {
        key: [v for v in val if v != "nan"] for key, val in schema_dict.items()
    }

    skills = [
        [
            {"name": str(v), "section": str(key)}
            for key, val in schema_dict.items()
            for v in val
        ]
    ]

    response = {"skills": skills}

    return response
