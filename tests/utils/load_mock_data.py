import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from app.utils.neo4j_connect import Neo4jConnection  # noqa: E402


def load_neo4j():
    """
    Load mock data into Neo4j
    """
    queries = [
        "CREATE CONSTRAINT ON (c:Consultant) ASSERT c.email IS UNIQUE",
        "CREATE CONSTRAINT ON (s:Skill) ASSERT s.name IS UNIQUE",
        """
        LOAD CSV WITH HEADERS FROM 'file:///mock_skills_data.csv' AS row
        MERGE (c:Consultant {name: row.name, email: row.email})
        MERGE (s:Skill {name: row.skill, category: row.category})
        MERGE (c)-[:KNOWS]->(s)
        """,
    ]

    conn = Neo4jConnection()

    for query in queries:
        conn.query(query)

    conn.close()


if __name__ == "__main__":
    load_neo4j()
