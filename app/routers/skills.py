from typing import Any, Optional

from fastapi import APIRouter, HTTPException

from app.models.skills import Skill, SkillList
from app.utils.neo4j_connect import Neo4jConnection

skills_router = APIRouter(prefix="/skills", tags=["Skills"])


@skills_router.get("/", response_model=SkillList)
async def list_all_skills(category: Optional[str] = None) -> Any:
    """
    Returns a list of all skills.

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
            WITH collect(distinct {name: s.name, category: s.category}) as skillsOut
            RETURN skillsOut
            """,
        ]
    )

    conn = Neo4jConnection()
    result = conn.query(query, parameters={"category": category})
    conn.close()

    return {"skills": result[0][0]}


@skills_router.get("/{skill_name}")
async def get_skill(skill_name: str) -> Any:
    """
    Returns a single skill using its name.

    Parameters
    ----------
    skill_name : str
        The name of the skill to return

    Returns
    -------
    Skill
    """
    query = """
    MATCH (s:Skill {name: $skill_name})
    UNWIND s as skills
    WITH collect(distinct {name: s.name, category: s.category}) as skillsOut
    RETURN skillsOut
    """

    conn = Neo4jConnection()
    result = conn.query(query, parameters={"skill_name": skill_name})
    conn.close()

    if not result[0][0]:
        raise HTTPException(status_code=404, detail="Skill not found")

    return {"skill": result[0][0]}


@skills_router.post("/")
async def add_skill(skill: Skill) -> Any:
    """
    Adds a new skill to the database.

    Parameters
    ----------
    skill : Skill
        The skill to add

    Returns
    -------
    Skill
    """
    query = """
    MERGE (s:Skill {name: $skill, category: $category})
    RETURN s
    """
    conn = Neo4jConnection()
    result = conn.query(
        query, parameters={"skill": skill.name, "category": skill.category}
    )
    conn.close()

    return {"message": "Skill added successfully", "result": result[0]}


@skills_router.delete("/{skill_name}")
async def delete_skill(skill_name: str) -> Any:
    """
    Deletes a skill from the database.

    Parameters
    ----------
    skill_name : str
        The name of the skill to delete

    Returns
    -------
    Skill
    """
    query = """
    MATCH (s:Skill {name: $skill})
    DETACH DELETE s
    RETURN s
    """
    conn = Neo4jConnection()
    result = conn.query(query, parameters={"skill": skill_name})
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Skill not found")

    return {"message": "Skill deleted successfully", "result": result[0]}
