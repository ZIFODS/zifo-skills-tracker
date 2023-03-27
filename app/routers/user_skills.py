from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app import config
from app.models.common import Message
from app.models.skills import Skill, SkillCreate, SkillList
from app.routers.auth import access_token_cookie_scheme
from app.utils.neo4j_connect import Neo4jConnection
from app.utils.security.providers import AzureAuthProvider

user_skills_router = APIRouter(prefix="/user/skills", tags=["User Skills"])


@user_skills_router.get("/")
async def list_user_skills(
    category: Optional[str] = None,
    external_access_token: str = Depends(access_token_cookie_scheme),
) -> SkillList:
    """
    Returns a list of skills for the current user.

    Returns
    -------
    SkillList
    """
    if not config.PROD_ENV:
        email = "anthony_hopkins@gmail.com"

    else:
        provider = AzureAuthProvider()
        external_user = await provider.get_user(
            external_access_token=external_access_token
        )
        email = external_user.email

    match = "MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill)"
    if category:
        match = "MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill {category: $category})"

    query = " ".join(
        [
            match,
            """
            UNWIND s as skills
            WITH COLLECT(DISTINCT {name: s.name, type: labels(s)[0],  category: s.category}) as skillsOut
            RETURN skillsOut
            """,
        ]
    )

    conn = Neo4jConnection()
    result = conn.query(query, email=email, category=category)
    conn.close()

    return SkillList(items=result[0][0])


@user_skills_router.get("/{skill_name:path}")
async def get_user_skill(
    skill_name: str,
    external_access_token: str = Depends(access_token_cookie_scheme),
) -> Skill:
    """
    Returns a skill if it is associated with the current user.

    Parameters
    ----------
    skill_name : str
        The name of the skill to return

    Returns
    -------
    Skill

    Raises
    ------
    HTTPException
        404 if the skill is not linked to the current user
    """
    if not config.PROD_ENV:
        email = "anthony_hopkins@gmail.com"

    else:
        provider = AzureAuthProvider()
        external_user = await provider.get_user(
            external_access_token=external_access_token
        )
        email = external_user.email

    query = """
    MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill {name: $name})
    WITH {name: s.name, type: labels(s)[0],  category: s.category} as skillOut
    RETURN skillOut
    """

    conn = Neo4jConnection()
    result = conn.query(query, email=email, name=skill_name)
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Skill not found for user")

    return result[0][0]


@user_skills_router.post("/")
async def create_user_skill(
    skills: list[SkillCreate],
    external_access_token: str = Depends(access_token_cookie_scheme),
) -> SkillList:
    """
    Creates a relationship between a skill and the current user.

    Parameters
    ----------
    skills : list[SkillCreate]
        The skills to link to the current user

    Returns
    -------
    Skill

    Raises
    ------
    HTTPException
        404 if any skill is already linked to the current user
    """
    if not config.PROD_ENV:
        email = "anthony_hopkins@gmail.com"

    else:
        provider = AzureAuthProvider()
        external_user = await provider.get_user(
            external_access_token=external_access_token
        )
        email = external_user.email

    skills = [s.dict() for s in skills]

    conn = Neo4jConnection()
    exists_query = """
    UNWIND $skills as skills
    MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill {name: skills.name})
    RETURN s
    """
    result = conn.query(exists_query, email=email, skills=skills)
    conn.close()
    if result:
        skill_names_linked = ", ".join([r[0]["name"] for r in result])
        raise HTTPException(
            status_code=409,
            detail=f"The following skills are already linked to the user: {skill_names_linked}",
        )

    query = """
    UNWIND $skills as skill
    MATCH (s:Skill {name: skill.name}), (c:Consultant {email: $email})
    MERGE (c)-[:KNOWS]->(s)
    WITH {name: s.name, type: labels(s)[0],  category: s.category} as skillsMerged
    RETURN COLLECT(skillsMerged) as skillsOut
    """
    conn = Neo4jConnection()
    result = conn.query(query, email=email, skills=skills)
    conn.close()

    if not result:
        raise HTTPException(
            status_code=404, detail="Skill not found and could not be linked to user"
        )

    return SkillList(items=result[0][0])


@user_skills_router.delete("/")
async def delete_user_skill(
    skill_names: list[str] = Query(),
    external_access_token: str = Depends(access_token_cookie_scheme),
) -> Message:
    """
    Removes the relationship between a skill and the current user.

    Parameters
    ----------
    skill_names : list[str]
        The names of the skills to delete

    Returns
    -------
    Message

    Raises
    ------
    HTTPException
        404 if the skill is not found for the current user
    """
    if not config.PROD_ENV:
        email = "anthony_hopkins@gmail.com"

    else:
        provider = AzureAuthProvider()
        external_user = await provider.get_user(
            external_access_token=external_access_token
        )
        email = external_user.email

    exists_query = """
    UNWIND $skill_names as skill_name
    MATCH (c:Consultant {email: $email})-[:KNOWS]->(s:Skill {name: skill_name})
    RETURN s
    """
    conn = Neo4jConnection()
    result = conn.query(exists_query, email=email, skill_names=skill_names)
    conn.close()
    if len(result) != len(skill_names):
        skill_names_linked = [r[0]["name"] for r in result]
        skill_names_not_linked = ", ".join([s for s in skill_names if s not in skill_names_linked])
        raise HTTPException(
            status_code=409,
            detail=f"The following skills are not linked to the user: {skill_names_not_linked}",
        )

    query = """
        UNWIND $skill_names as skill_name
        MATCH (c:Consultant {email: $email})-[r:KNOWS]->(s:Skill {name: skill_name})
        WITH r, {name: s.name, type: labels(s)[0],  category: s.category} as skillOut
        DELETE r
        RETURN skillOut
        """

    conn = Neo4jConnection()
    result = conn.query(
        query,
        email=email,
        skill_names=skill_names,
    )
    conn.close()
    
    skill_names_removed = ", ".join([r[0]["name"] for r in result])

    return Message(message=f"Removed {skill_names_removed} for user {email}")
