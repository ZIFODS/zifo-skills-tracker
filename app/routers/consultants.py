from typing import List
from fastapi import APIRouter, Query
from app.utils import NEO4J_TO_D3_CYPHER

from pipeline.src.neo4j_connect import Neo4jConnection

consultants_router = APIRouter()

@consultants_router.get("/", name="Filter by skills")
async def filter_consultants_by_skills(skills: List[str] = Query(default=...)):
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    query = "MATCH p=(c:Consultant)-[:KNOWS]->(s) "
    for i, skill in enumerate(skills):
        if i == 0:
            query += "where "
        query += f"s.Name = '{skill}'"
        if i != len(skills) - 1:
            query += " AND "

    query += NEO4J_TO_D3_CYPHER

    result = conn.query(query)
    
    conn.close()

    return result[0][0]