import base64
import json
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.logic.cypher import (
    compile_results_with_nodes,
    compile_results_with_nodes_and_links,
    determine_all_categories_hidden,
    remove_skill_nodes_with_hidden_categories,
)
from app.models.graph import GraphData, Rule
from app.utils.neo4j_connect import Neo4jConnection

logger = logging.getLogger(__name__)

graph_router = APIRouter(prefix="/graph", tags=["Graph"])


@graph_router.get("/", name="Get graph data")
async def filter_graph(
    skills: Optional[str] = Query(default=None),
    consultant: Optional[str] = None,
    hidden_categories: list[str] = Query(default=[]),
) -> GraphData:
    """
    Filter consultants and their associated skills using either a list of skill rules or a
    consultant name.
    Skills within defined categories can be omitted from the results.
    If no filtering is defined, return empty graph.

    Arguments
    ---------
    skills : Optional[str]
        base64 encoded string representing a list of Rule objects.
        See Rule model for more details.
    consultant : Optional[str]
        full name of Consultant
    hidden_categories : list[str]
        names of categories to be omitted from results

    Returns
    -------
    output : GraphData
        nodes and links of filtered graph data

    Raises
    ------
    HTTPException
        404 if no consultant is found with the name provided
    """
    conn = Neo4jConnection()

    all_hidden = determine_all_categories_hidden(conn, hidden_categories)

    if skills:
        rules_str = base64.urlsafe_b64decode(skills)
        rules = [Rule(**rule) for rule in json.loads(rules_str)]
        query = process_skills_query(rules, hidden_categories, all_hidden)
        result = conn.query(query)

        result[0][0]["nodes"].sort(key=lambda x: x.get("name"))
        result[0][0]["links"].sort(key=lambda x: x.get("name"))

        output = result[0][0]

    elif consultant:
        query = process_consultant_query(consultant, hidden_categories, all_hidden)
        result = conn.query(query)

        result[0][0]["nodes"].sort(key=lambda x: x.get("name"))
        result[0][0]["links"].sort(key=lambda x: x.get("name"))

        output = result[0][0]
        if not output["nodes"]:
            raise HTTPException(
                status_code=404,
                detail="A Consultant could not be found with the name provided.",
            )

    else:
        output = {"nodes": [], "links": []}

    conn.close()

    return output


def process_skills_query(
    rules: list[Rule], hidden_categories: list[str], all_hidden: bool
) -> str:
    """
    Process a list of skill rules and return a query to filter the graph data.

    Parameters
    ----------
    rules : list[Rule]
        list of Rule objects
    hidden_categories : list[str]
        names of categories to be omitted from results
    all_hidden : bool
        True if all categories are hidden. In this case, just collect consultants.

    Returns
    -------
    query : str
        query to filter graph data
    """
    query = "MATCH (c:Consultant)-[:KNOWS]->(:Skill)"

    brackets_open = False
    for rule in reversed(rules):
        if rule.parenthesis == "[":
            brackets_open = True
            break
        elif rule.parenthesis == "]":
            break

    for i, rule in enumerate(rules):
        skill_filter = " (c)-[:KNOWS]->(:Skill {name: '" + rule.name + "'})"

        if i == 0:
            query += " WHERE"

        if rule.parenthesis == "[":
            if i != 0:
                query += f" {rule.operator}"
            query += " ("

        if i != 0:
            if rule.parenthesis != "[":
                query += f" {rule.operator}"

        query += skill_filter

        if rule.parenthesis == "]" or (i == len(rules) - 1 and brackets_open):
            query += ")"

    # compile final results
    if all_hidden:
        query += " MATCH p=(c)"
        query += compile_results_with_nodes()

    else:
        query += " MATCH p=(c)-[:KNOWS]-(s:Skill)"
        # remove any hidden categories
        if hidden_categories:
            query += remove_skill_nodes_with_hidden_categories(hidden_categories)
        query += compile_results_with_nodes_and_links()

    return query


def process_consultant_query(
    consultant: str, hidden_categories: list[str], all_hidden: bool
) -> str:
    """
    Process a consultant name and return a query to filter the graph data.

    Parameters
    ----------
    consultant : str
        full name of Consultant
    hidden_categories : list[str]
        names of categories to be omitted from results
    all_hidden : bool
        True if all categories are hidden. In this case, just collect consultants.

    Returns
    -------
    query : str
        query to filter graph data
    """
    query = ""

    # collect nodes
    if not all_hidden:
        query += (
            "MATCH p=(c:Consultant {name: '" + consultant + "'})-[:KNOWS]->(s:Skill)"
        )
    else:
        query += "MATCH p=(c:Consultant {name: '" + consultant + "'})"

    # compile final results
    if all_hidden:
        query += compile_results_with_nodes()

    else:
        # remove any hidden categories
        if hidden_categories:
            query += remove_skill_nodes_with_hidden_categories(hidden_categories)
        query += compile_results_with_nodes_and_links()

    return query
