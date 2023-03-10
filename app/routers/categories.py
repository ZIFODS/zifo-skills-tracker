from fastapi import APIRouter

from app.models.skills import CategoryList
from app.utils.neo4j_connect import Neo4jConnection

categories_router = APIRouter(prefix="/categories", tags=["Skill categories"])


@categories_router.get("/")
async def list_all_categories() -> CategoryList:
    """
    Returns a list of all skill categories sorted alphabetically.

    Returns
    -------
    CategoryList
    """
    query = """
    MATCH (s:Skill)
    UNWIND s as skills
    WITH COLLECT(DISTINCT s.category) as categoriesOut
    RETURN categoriesOut
    """

    conn = Neo4jConnection()
    result = conn.query(query)
    conn.close()

    if not result:
        return CategoryList(items=[])

    categories = result[0][0]
    categories.sort()

    return CategoryList(items=categories)
