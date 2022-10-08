def neo4j_to_d3_cypher(final_char):
    query = f" unwind nodes(p{final_char}) as n{final_char} unwind relationships(p{final_char}) as r{final_char}"

    query += " with collect( distinct {"
    query += f"id: ID(n{final_char}), name: n{final_char}.Name, group: labels(n{final_char})[0]"
    query += "}) as nzz,"

    query += " collect( distinct {"
    query += f"id: ID(r{final_char}), source: ID(startnode(r{final_char})), target: ID(endnode(r{final_char}))"
    query += "}) as rzz"
    
    query += " RETURN {nodes: nzz, links: rzz}"
    return query