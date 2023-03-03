from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.models.auth import ExternalToken
from app.models.skills import Skill
from app.routers.auth import access_token_cookie_scheme
from app.utils.neo4j_connect import Neo4jConnection
from app.utils.security.providers import AzureAuthProvider

user_skills_router = APIRouter(prefix="/user/skills", tags=["User Skills"])


@user_skills_router.get("/")
async def list_user_skills(
    category: Optional[str] = None,
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

    match = "MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill)"
    if category:
        match = "MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill {category: $category})"

    query = " ".join(
        [
            match,
            """
            UNWIND s as skills
            WITH collect(distinct {name: s.name, category: s.category}) as skillsOut
            RETURN skillsOut
            """,
        ]
    )

    conn = Neo4jConnection()
    result = conn.query(query, parameters={"email": email, "category": category})
    conn.close()

    return {"skills": result[0][0]}


@user_skills_router.get("/{skill_name}")
async def get_user_skill(
    skill_name: str,
    external_access_token: ExternalToken = Depends(access_token_cookie_scheme),
) -> Any:
    """
    Returns a skill for a given user.

    Parameters
    ----------
    skill_name : str
        The name of the skill to return

    Returns
    -------
    Skill
    """
    provider = AzureAuthProvider()
    external_user = await provider.get_user(external_access_token=external_access_token)
    email = external_user.email

    query = """
    MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill {name: $skill_name})
    UNWIND s as skills
    WITH collect(distinct {name: s.name, category: s.category}) as skillsOut
    RETURN skillsOut
    """

    conn = Neo4jConnection()
    result = conn.query(query, parameters={"email": email, "skill_name": skill_name})
    conn.close()

    if not result[0][0]:
        raise HTTPException(status_code=404, detail="Skill not found for user")

    return {"skill": result[0][0]}


@user_skills_router.post("/")
async def add_user_skill(
    skill: Skill,
    external_access_token: ExternalToken = Depends(access_token_cookie_scheme),
) -> Any:
    """
    Adds a skill for a given user.

    Parameters
    ----------
    skill : Skill
        The skill to add

    Returns
    -------
    Skill
    """
    provider = AzureAuthProvider()
    external_user = await provider.get_user(external_access_token=external_access_token)
    email = external_user.email

    query = """
    MATCH (c:Consultant {email: $email}), (s:Skill {name: $name, category: $category})
    MERGE p = (c)-[r:KNOWS]->(s)
    RETURN p
    """

    conn = Neo4jConnection()
    result = conn.query(
        query,
        parameters={"email": email, "name": skill.name, "category": skill.category},
    )
    conn.close()

    if not result:
        raise HTTPException(
            status_code=404, detail="Skill not found and could not be linked to user"
        )

    return {"message": "Skill added successfully", "result": result[0]}


@user_skills_router.delete("/{skill_name}")
async def delete_user_skill(
    skill_name: str,
    external_access_token: ExternalToken = Depends(access_token_cookie_scheme),
) -> Any:
    """
    Deletes a skill for a given user.

    Parameters
    ----------
    skill_name : str
        The name of the skill to delete

    Returns
    -------
    Skill
    """
    provider = AzureAuthProvider()
    external_user = await provider.get_user(external_access_token=external_access_token)
    email = external_user.email

    query = """
        MATCH p = (c:Consultant {email: $email})-[r:KNOWS]->(s:Skill {name: $skill})
        DELETE r
        RETURN p
        """

    conn = Neo4jConnection()
    result = conn.query(
        query,
        parameters={"email": email, "skill": skill_name},
    )
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Skill not found for user")

    return {"message": "Skill deleted successfully", "result": result[0]}
