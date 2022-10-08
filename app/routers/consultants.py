from typing import List
from fastapi import APIRouter, Query
from app.utils import neo4j_to_d3_cypher

from pipeline.src.neo4j_connect import Neo4jConnection

consultants_router = APIRouter()

# MATCH pa=(c:Consultant)-[:KNOWS]-(s) where s.Name = 'REACT' 
# unwind nodes(pa) as na
# MATCH pb=(na)-[:KNOWS]->(t) where t.Name = "REDUX"
# unwind nodes(pb) as nb unwind relationships(pb) as rb
# with collect( distinct {id: ID(nb), name: nb.Name, group: labels(nb)[0]}) as nl, 
# collect( distinct {id: ID(rb), source: ID(startnode(rb)), target: ID(endnode(rb))}) as rl
# RETURN {nodes: nl, links: rl}

def char(num: int):
    return chr(num + 97)

@consultants_router.get("/", name="Filter by skills")
async def filter_consultants_by_skills(
    skills: List[str] = Query(default=...),
    hidden_groups: List[str] = Query(default=[])
    ):
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    query = "MATCH pa=(c:Consultant)-[:KNOWS]->(sa) "
    for i, skill in enumerate(skills):
        if i == 0:
            query += f"where s{char(i)}.Name = '{skill}'"

        else:
            query += f" unwind nodes(p{char(i-1)}) as n{char(i-1)}"
            query += f" MATCH p{char(i)}=(n{char(i-1)})-[:KNOWS]->(s{char(i)}) where s{char(i)}.Name = '{skill}'"

    penult_char = char(len(skills) - 1)
    final_char = char(len(skills))

    query += f"unwind nodes(p{penult_char}) as n{penult_char} "
    query += f" MATCH p{final_char}=(n{penult_char})-[:KNOWS]->()"

    if hidden_groups:
        query += f" WHERE NONE(n IN nodes(p{final_char}) WHERE"
        for i, group in enumerate(hidden_groups):
            query += f" n:{group}"
            if i != len(hidden_groups) - 1:
                query += " OR"
            else:
                query += ")"

    query += neo4j_to_d3_cypher(final_char)

    print(query)

    result = conn.query(query)
    
    conn.close()

    return result[0][0]