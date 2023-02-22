from typing import Any

from fastapi import APIRouter, Depends

from app.models.auth import ExternalToken
from app.models.skills import SkillList
from app.routers.auth import access_token_cookie_scheme
from app.utils.neo4j_connect import Neo4jConnection
from app.utils.security.providers import AzureAuthProvider
from app.utils.skills import pull_skills_schema_from_s3

skills_router = APIRouter(prefix="/skills", tags=["Skills"])


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
            {"name": str(v), "category": str(key)}
            for key, val in schema_dict.items()
            for v in val
        ]
    ]

    response = {"skills": skills}

    return response


@skills_router.get("/user")
async def list_user_skills(
    external_access_token: ExternalToken = Depends(access_token_cookie_scheme),
) -> Any:
    """
    Returns a list of skills for a given user.

    Returns
    -------
    SkillList
    """
    provider = AzureAuthProvider()
    external_user = await provider.get_user(external_access_token=external_access_token)
    email = external_user.email

    query = """
    MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill)
    UNWIND s as skills
    WITH collect(distinct {name: s.name, category: s.category}) as skillsOut
    RETURN skillsOut
    """

    conn = Neo4jConnection()
    result = conn.query(query, parameters={"email": email})
    conn.close()

    print(result[0][0])

    return {"skills": result[0][0]}
