import base64
import json
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.logic.brackets import (
    OrStatusProcesser,
    determine_effective_bracket_indexes,
    increment_path_count,
    is_index_at_end_of_bracket,
)
from app.logic.cypher import (
    compile_results_with_nodes,
    compile_results_with_nodes_and_links,
    determine_all_categories_hidden,
    generate_intersect_or_union_query,
    match_all_consultants,
    match_all_consultants_with_knows_relationship,
    match_consultant_with_name,
    match_consultant_with_name_with_knows_relationship,
    match_nodes_from_previous_nodes_with_knows_relationship,
    or_skill_with_name,
    remove_skill_nodes_with_hidden_categories,
    unwind_nodes,
    where_skill_has_name,
)
from app.models.graph import GraphData, Rule
from app.utils.neo4j_connect import Neo4jConnection

graph_router = APIRouter(prefix="/graph", tags=["Graph"])

# Example of a skills query:
#
# Get consultants who know BIOVIA ONELab along with their known skills but don't return skills
# in ScienceApps or Process categories:
#
# MATCH pa=(c:Consultant)-[:KNOWS]->(sa) where sa.Name = 'BIOVIA ONELab'
# unwind nodes(pa) as na
# MATCH pb=(na)-[:KNOWS]->()
# WHERE NONE(n IN nodes(pb) WHERE n:ScienceApps OR n:Process)
# unwind nodes(pb) as nb unwind relationships(pb) as rb
# with collect( distinct {id: ID(nb), name: nb.Name, group: labels(nb)[0]}) as nzz,
# collect( distinct {id: ID(rb), source: ID(startnode(rb)), target: ID(endnode(rb))}) as rzz
# RETURN {nodes: nzz, links: rzz}


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
        output = result[0][0]

    elif consultant:
        query = process_consultant_query(consultant, hidden_categories, all_hidden)
        result = conn.query(query)
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
    bracket_idx_list = determine_effective_bracket_indexes(rules)

    path_count = 0
    idx_path_num = {}
    or_status_processor = OrStatusProcesser()

    query = match_all_consultants_with_knows_relationship(path_count)

    for i, rule in enumerate(rules):

        name = rule.name
        parenthesis = rule.parenthesis

        idx_path_num[i] = path_count

        index_at_end_of_bracket = is_index_at_end_of_bracket(i, bracket_idx_list)

        or_status = or_status_processor.process(i, rules)
        is_or, start_or, end_or = or_status

        # match
        if i != 0:
            if parenthesis == "[" or start_or:
                query += match_all_consultants_with_knows_relationship(path_count)

            elif not is_or:
                query += match_nodes_from_previous_nodes_with_knows_relationship(
                    path_count
                )

        # where
        if not is_or or start_or:
            query += where_skill_has_name(path_count, name)

        # or_q
        if is_or and not start_or:
            query += or_skill_with_name(path_count, name)

        # unwind_q
        if not is_or or end_or:
            query += unwind_nodes(path_count)

        # intersection/union
        if index_at_end_of_bracket:
            query += generate_intersect_or_union_query(
                i, rules, bracket_idx_list, idx_path_num
            )

        # increment path count
        path_count = increment_path_count(
            path_count, or_status, parenthesis, index_at_end_of_bracket
        )

    # collect final nodes
    if all_hidden:
        query += match_all_consultants(path_count)
        query += compile_results_with_nodes(path_count)

    else:
        query += match_nodes_from_previous_nodes_with_knows_relationship(path_count)
        # remove any hidden categories
        if hidden_categories:
            query += remove_skill_nodes_with_hidden_categories(
                path_count, hidden_categories
            )
        query += compile_results_with_nodes_and_links(path_count)

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
    path_count = 0
    query = ""

    # collect nodes
    if not all_hidden:
        query += match_consultant_with_name_with_knows_relationship(
            path_count, consultant
        )
    else:
        query += match_consultant_with_name(path_count, consultant)

    # compile final results
    if all_hidden:
        query += compile_results_with_nodes(path_count)

    else:
        # remove any hidden categories
        if hidden_categories:
            query += remove_skill_nodes_with_hidden_categories(
                path_count, hidden_categories
            )
        query += compile_results_with_nodes_and_links(path_count)

    return query
