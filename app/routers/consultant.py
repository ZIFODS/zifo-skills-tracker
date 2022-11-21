from fastapi import APIRouter, HTTPException

from app.models.graph import GraphData
from pipeline.src.neo4j_connect import Neo4jConnection
from app.logic.cypher import (
    match_consultant_with_name_with_knows_relationship,
    compile_results_with_nodes_and_links,
)

consultant_router = APIRouter()

@consultant_router.get("/", name="Filter by consultant")
async def filter_with_consultant(consultant_name: str) -> GraphData:
    """
    Search for a Consultant given their full name.

    Arguments
    ---------
    consultant_name : str
        full name of Consultant

    Returns
    -------
    result : GraphData
        nodes and links of filtered graph data
    """
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    path_count = 0

    query = match_consultant_with_name_with_knows_relationship(
        path_count, consultant_name
    )
    query += compile_results_with_nodes_and_links(path_count)

    print(query)

    result = conn.query(query)

    conn.close()

    output = result[0][0]
    if not output["nodes"]:
        raise HTTPException(status_code=404, detail="A Consultant could not be found with the name provided.")

    return output
