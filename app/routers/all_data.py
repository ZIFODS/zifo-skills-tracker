from fastapi import APIRouter
import json

from app.logic.cypher import match_all_consultants_with_knows_relationship, compile_results_with_nodes_and_links
from pipeline.src.neo4j_connect import Neo4jConnection

all_data_router = APIRouter()

@all_data_router.get("/", name="Get all nodes and edges")
async def get_all_nodes_edges():

    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    path_count = 0

    # Get all Consultants and their skills
    query = match_all_consultants_with_knows_relationship(path_count)
    query += compile_results_with_nodes_and_links(path_count)

    result = conn.query(query)
    
    conn.close()

    return result[0][0]