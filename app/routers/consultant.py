from fastapi import APIRouter, HTTPException, Query

from app.models.graph import GraphData
from pipeline.src.neo4j_connect import Neo4jConnection
from app.logic.cypher import (
    determine_all_categories_hidden,
    match_consultant_with_name_with_knows_relationship,
    match_consultant_with_name,
    remove_nodes_with_hidden_categories,
    compile_results_with_nodes,
    compile_results_with_nodes_and_links,
)

consultant_router = APIRouter()


@consultant_router.get("/", name="Filter by consultant")
async def filter_with_consultant(
    consultant_name: str, hidden_categories: list[str] = Query(default=[])
) -> GraphData:
    """
    Search for a Consultant given their full name.
    Skills within defined categories can be omitted from the results.

    Arguments
    ---------
    consultant_name : str
        full name of Consultant
    hidden_categories : list[str]
        names of categories to be omitted from results

    Returns
    -------
    result : GraphData
        nodes and links of filtered graph data
    """
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    all_hidden = determine_all_categories_hidden(conn, hidden_categories)

    path_count = 0
    query = ""

    # collect nodes
    if not all_hidden:
        query += match_consultant_with_name_with_knows_relationship(
            path_count, consultant_name
        )
    else:
        query += match_consultant_with_name(path_count, consultant_name)

    # remove any hidden categories
    if hidden_categories:
        query += remove_nodes_with_hidden_categories(path_count, hidden_categories)

    # compile final results
    if all_hidden:
        query += compile_results_with_nodes(path_count)
    else:
        query += compile_results_with_nodes_and_links(path_count)

    print(query)

    result = conn.query(query)

    conn.close()

    output = result[0][0]
    if not output["nodes"]:
        raise HTTPException(
            status_code=404,
            detail="A Consultant could not be found with the name provided.",
        )

    return output
