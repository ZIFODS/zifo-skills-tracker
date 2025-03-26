import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.utils.neo4j_connect import Neo4jConnection  # noqa: E402


def load_neo4j(reset: bool = False, empty: bool = False):
    """
    load_neo4j(reset: bool = False, empty: bool = False)
    Load mock data into Neo4j

    Function to handle the mock data DB. It can be called with no parameters to create constraints and load mock data
    into an empty DB (needed after loading the Neo4J docker container).

    Parameters
    ----------
    reset : bool
        If True, delete existing DB data/constraints and then re-create constraints and load data.
    empty : bool
        If True, delete DB data/constraints only. Ignored if reset = True.
    """
    queries = [
        "MATCH (n) DETACH DELETE n",
        "CALL apoc.schema.assert({},{},true) YIELD label, key RETURN *",
        "CREATE CONSTRAINT ON (c:Consultant) ASSERT c.email IS UNIQUE",
        "CREATE CONSTRAINT ON (c:Consultant) ASSERT c.uid IS UNIQUE",
        "CREATE CONSTRAINT ON (s:Skill) ASSERT s.name IS UNIQUE",
        "CREATE CONSTRAINT ON (s:Skill) ASSERT s.uid IS UNIQUE",
        "CREATE CONSTRAINT ON (r:KNOWS) ASSERT r.uid IS UNIQUE",
        f"""
        LOAD CSV WITH HEADERS FROM 'file:///mock_skills_data.csv' AS row
        MERGE (c:Consultant {{uid: row.cid, name: row.name, email: row.email}})
        MERGE (s:Skill {{uid: row.sid, name: row.skill, category: row.category}})
        MERGE (c)-[:KNOWS {{uid: row.rid}}]->(s)
        """,
    ]

    if not reset and not empty:
        queries = [
            queries[2],
            queries[3],
            queries[4],
            queries[5],
            queries[6],
            queries[7],
        ]
    elif empty:
        queries = [queries[0], queries[1]]

    conn = Neo4jConnection()

    for query in queries:
        conn.query(query)

    conn.close()


if __name__ == "__main__":
    load_neo4j()
