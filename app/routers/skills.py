from fastapi import APIRouter
import json
from pipeline.src.js_skills import neo4j_to_d3_json

from pipeline.src.neo4j_connect import Neo4jConnection

skills_router = APIRouter()

@skills_router.get("/", name="Get all nodes and edges")
async def get_all_nodes_edges():
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    result = conn.query('''CALL apoc.export.json.all(null, {stream: true})
        YIELD file, nodes, relationships, properties, data
        RETURN file, nodes, relationships, properties, data'''
    )

    conn.close()

    skills_str = "[" + result[0][4].replace("\n", ",") + "]"
    skills_json = json.loads(skills_str)

    d3_json = neo4j_to_d3_json(skills_json)

    return d3_json