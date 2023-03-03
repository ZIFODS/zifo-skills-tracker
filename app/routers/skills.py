import base64
from fastapi import APIRouter, Query
import json

from app.models.graph import GraphData
from pipeline.src.neo4j_connect import Neo4jConnection
from app.logic.brackets import (
    determine_effective_bracket_indexes,
    OrStatusProcesser,
    is_index_at_end_of_bracket,
    increment_path_count,
)
from app.logic.cypher import (
    determine_all_categories_hidden,
    match_all_consultants_with_knows_relationship,
    match_nodes_from_previous_nodes,
    match_nodes_from_previous_nodes_with_knows_relationship,
    where_skill_has_name,
    or_skill_with_name,
    unwind_nodes,
    generate_intersect_or_union_query,
    remove_nodes_with_hidden_categories,
    compile_results_with_nodes,
    compile_results_with_nodes_and_links,
)

skills_router = APIRouter()

"""
Get consultants who know BIOVIA ONELab along with their known skills but don't return skills in ScienceApps or Process categories:

MATCH pa=(c:Consultant)-[:KNOWS]->(sa) where sa.Name = 'BIOVIA ONELab'
unwind nodes(pa) as na
MATCH pb=(na)-[:KNOWS]->() 
WHERE NONE(n IN nodes(pb) WHERE n:ScienceApps OR n:Process) 
unwind nodes(pb) as nb unwind relationships(pb) as rb 
with collect( distinct {id: ID(nb), name: nb.Name, group: labels(nb)[0]}) as nzz, 
collect( distinct {id: ID(rb), source: ID(startnode(rb)), target: ID(endnode(rb))}) as rzz 
RETURN {nodes: nzz, links: rzz}
"""

@skills_router.get("/", name="Filter by skills")
async def filter_consultants_with_skills(
    skills: str = Query(default=...), hidden_categories: list[str] = Query(default=[])
) -> GraphData:
    """
    Filter for consultants that know skills according to a set of defined AND/OR rules.
    Skills within defined categories can be omitted from the results.

    Arguments
    ---------
    skills : str
        base64 encoded string representing a list of Rule objects.
        See Rule model for more details.
    hidden_categories : list[str]
        names of categories to be omitted from results

    Returns
    -------
    result : GraphData
        nodes and links of filtered graph data
    """
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    rules_str = base64.urlsafe_b64decode(skills)
    rules = json.loads(rules_str)

    all_hidden = determine_all_categories_hidden(conn, hidden_categories)

    bracket_idx_list = determine_effective_bracket_indexes(rules)

    path_count = 0
    idx_path_num = {}
    or_status_processor = OrStatusProcesser()

    query = match_all_consultants_with_knows_relationship(path_count)

    for i, rule in enumerate(rules):

        name = rule["name"]
        parenthesis = rule["parenthesis"]

        idx_path_num[i] = path_count

        index_at_end_of_bracket = is_index_at_end_of_bracket(i, bracket_idx_list)

        or_status = or_status_processor.process(i, rules)
        is_or, start_or, end_or = or_status

        ## match
        if i != 0:
            if parenthesis == "[" or start_or:
                query += match_all_consultants_with_knows_relationship(path_count)

            elif not is_or:
                query += match_nodes_from_previous_nodes_with_knows_relationship(
                    path_count
                )

        ## where
        if not is_or or start_or:
            query += where_skill_has_name(path_count, name)

        ## or_q
        if is_or and not start_or:
            query += or_skill_with_name(path_count, name)

        ## unwind_q
        if not is_or or end_or:
            query += unwind_nodes(path_count)

        ## intersection/union
        if index_at_end_of_bracket:
            query += generate_intersect_or_union_query(
                i, rules, bracket_idx_list, idx_path_num
            )

        # increment path count
        path_count = increment_path_count(
            path_count, or_status, parenthesis, index_at_end_of_bracket
        )

    # collect final nodes
    if not all_hidden:
        query += match_nodes_from_previous_nodes_with_knows_relationship(path_count)
    else:
        query += match_nodes_from_previous_nodes(path_count)

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

    return result[0][0]
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
