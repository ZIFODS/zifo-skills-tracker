from typing import List
from fastapi import APIRouter, Query

from pipeline.src.neo4j_connect import Neo4jConnection

consultants_router = APIRouter()

@consultants_router.get("/", name="Filter by skills")
async def filter_consultants_by_skills(skills: List[str] = Query(default=...)):
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    query = "MATCH (c:Consultant)-[:KNOWS]->(s) "
    for i, skill in enumerate(skills):
        if i == 0:
            query += "where "
        query += f"s.Name = '{skill}'"
        if i != len(skills) - 1:
            query += " AND "

    query += " return c,s"

    print(query)

    result = conn.query(query)
    
    conn.close()

    return result