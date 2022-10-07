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
async def filter_consultants_by_skills(skills: List[str] = Query(default=...)):
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    query = "MATCH pa=(c:Consultant)-[:KNOWS]->(sa) "
    for i, skill in enumerate(skills):
        if i == 0:
            query += f"where s{char(i)}.Name = '{skill}'"

        else:
            query += f" unwind nodes(p{char(i-1)}) as n{char(i-1)}"
            query += f" MATCH p{char(i)}=(n{char(i-1)})-[:KNOWS]->(s{char(i)}) where s{char(i)}.Name = '{skill}'"

    query += neo4j_to_d3_cypher(char(len(skills)))

    print(query)

    result = conn.query(query)
    
    conn.close()

    return result[0][0]