from app.utils.neo4j_connect import Neo4jConnection


def get_next_uid() -> int:
    query = """
    MATCH ((c:Consultant)-[r:KNOWS]-(s:Skill))
    RETURN Max(toInteger(s.uid)) as max_sid, Max(toInteger(c.uid)) as max_cid, Max(toInteger(r.uid)) as max_rid
    """

    conn = Neo4jConnection()
    result = conn.query(query)
    conn.close()

    next_id = max([result[0][0], result[0][1], result[0][2]]) + 1

    return next_id
