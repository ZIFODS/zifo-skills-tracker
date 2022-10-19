import base64
from typing import List
from fastapi import APIRouter, Query
from app.utils import neo4j_to_d3_cypher
import json

from pipeline.src.neo4j_connect import Neo4jConnection

consultants_router = APIRouter()

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

def char(num: int):
    return chr(num + 97)

@consultants_router.get("/", name="Filter by skills")
async def filter_consultants_by_skills(
    skills: str = Query(default=...),
    hidden_groups: List[str] = Query(default=[])
    ):
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    rules_str = base64.urlsafe_b64decode(skills)
    rules = json.loads(rules_str)

    all_hidden = False
    if hidden_groups:
        all_labels_result = conn.query("MATCH (n) RETURN distinct labels(n)")
        all_groups = [label.values("labels(n)")[0][0] for label in all_labels_result]
        if "Consultant" in all_groups:
            all_groups.remove("Consultant")

        all_groups.sort()
        hidden_groups.sort()
        if all_groups == hidden_groups:
            all_hidden = True

    path_count = 0
    initial_or = False
    end_or = False
    is_or = False
    query = "MATCH pa=(c:Consultant)-[:KNOWS]->(sa)"

    for i, rule in enumerate(rules):

        match_start = ""
        where_q = ""
        or_q = ""
        unwind_q = ""

        name = rule["name"]

        final_i = len(rules) - 1

        # Determine or sequence status
        if rule["operator"] == "AND":
            is_or = False
            initial_or = False

        if rule["operator"] == "OR":
            is_or = True
            if i == final_i:
                initial_or = False
                end_or = True
            elif rules[i+1]["operator"] != "OR":
                initial_or = False
                end_or = True

        if i != final_i:
            if rules[i+1]["operator"] == "OR":
                initial_or = True
                is_or = True
                end_or = False

        ## match
        if i != 0:
            if rule["parenthesis"] == "[" or initial_or:
                match_start = f" MATCH p{char(path_count)}=()-[:KNOWS]->(s{char(path_count)})"

            elif not is_or:
                match_start = f" MATCH p{char(path_count)}=(n{char(path_count-1)})-[:KNOWS]->(s{char(path_count)})"

        ## where
        if not is_or or initial_or:
            where_q = f" where s{char(path_count)}.Name = '{name}'"

        ## or_q
        if is_or and not initial_or:
            or_q = f" OR s{char(path_count)}.Name = '{name}'"

        ## unwind_q
        if not initial_or:
            unwind_q = f" unwind nodes(p{char(path_count)}) as n{char(path_count)}"

        # Move to next path
        if rule["parenthesis"] == "]":
            path_count += 1
        elif not is_or:
            path_count += 1
        elif end_or:
            path_count += 1

        query += match_start + where_q + or_q + unwind_q

    penult_char = char(path_count - 1)
    final_char = char(path_count)

    if not all_hidden:
        query += f" MATCH p{final_char}=(n{penult_char})-[:KNOWS]->()"
    else:
        query += f" MATCH p{final_char}=(n{penult_char})"
    
    if hidden_groups:
        query += f" WHERE NONE(n IN nodes(p{final_char}) WHERE"
        for i, group in enumerate(hidden_groups):
            query += f" n:{group}"
            if i != len(hidden_groups) - 1:
                query += " OR"
            else:
                query += ")"

    if all_hidden:
        query += f" unwind nodes(p{final_char}) as n{final_char}"
        query += " with collect( distinct {id: ID(n" + final_char + f"), name: n{final_char}.Name, group: labels(n{final_char})[0]" + "}) as nzz"
        query += " return {nodes: nzz, links: []}"

    else:
        query += neo4j_to_d3_cypher(final_char)

    print(query)

    result = conn.query(query)
    
    conn.close()

    return result[0][0]