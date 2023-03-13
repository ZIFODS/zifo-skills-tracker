from typing import Optional

from fastapi import APIRouter, HTTPException

from app.models.common import Message
from app.models.skills import Skill, SkillCreate, SkillList
from app.utils.neo4j_connect import Neo4jConnection

skills_router = APIRouter(prefix="/skills", tags=["Skills"])


@skills_router.get("/")
async def list_all_skills(category: Optional[str] = None) -> SkillList:
    """
    Returns a list of all skills sorted alphabetically by name.
    Optionally filter by category.

    Returns
    -------
    SkillList
    """
    match = "MATCH (s:Skill)"
    if category:
        match = "MATCH (s:Skill {category: $category})"

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
    result = conn.query(query, category=category)
    conn.close()

    skills = result[0][0]
    skills.sort(key=lambda x: x["name"])

    return SkillList(items=skills)


@skills_router.get("/{skill_name:path}")
async def get_skill(skill_name: str) -> Skill:
    """
    Returns a single skill using its name.

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
        If the skill is not found
    """
    query = """
    MATCH (s:Skill {name: $name})
    WITH {name: s.name, type: labels(s)[0],  category: s.category} as skillOut
    RETURN skillOut
    """

    conn = Neo4jConnection()
    result = conn.query(query, name=skill_name)
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Skill not found")

    return result[0][0]


@skills_router.post("/")
async def create_skill(skill: SkillCreate) -> Skill:
    """
    Add a new skill to the database.
    If the skill already exists, return a 409.

    Parameters
    ----------
    skill : SkillCreate
        The skill to add

    Returns
    -------
    Skill
    """
    conn = Neo4jConnection()
    exists_query = """
    MATCH (s:Skill {name: $name})
    RETURN s
    """
    result = conn.query(exists_query, name=skill.name)
    conn.close()
    if result:
        raise HTTPException(status_code=409, detail="Skill already exists")

    query = """
    MERGE (s:Skill {name: $name, category: $category})
    WITH {name: s.name, type: labels(s)[0],  category: s.category} as skillOut
    RETURN skillOut
    """
    conn = Neo4jConnection()
    result = conn.query(query, name=skill.name, category=skill.category)
    conn.close()

    return result[0][0]


@skills_router.delete("/{skill_name}")
async def delete_skill(skill_name: str) -> Message:
    """
    Deletes a skill from the database.

    Parameters
    ----------
    skill_name : str
        The name of the skill to delete

    Returns
    -------
    Message

    Raises
    ------
    HTTPException
        If the skill is not found
    """
    query = """
    MATCH (s:Skill {name: $skill})
    WITH s, {name: s.name, type: labels(s)[0],  category: s.category} as skillOut
    DETACH DELETE s
    RETURN skillOut
    """
    conn = Neo4jConnection()
    result = conn.query(query, skill=skill_name)
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Skill not found")

    return Message(message=f"Deleted skill {skill_name}")
