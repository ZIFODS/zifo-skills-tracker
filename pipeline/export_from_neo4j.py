import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from app.utils.neo4j_connect import Neo4jConnection  # noqa: E402

OUTPUT_FILE = "backup.csv"


def export_from_neo4j():
    """
    Export data from neo4j in neo4j import format.
    """
    query = """
    MATCH (c:Consultant)-[r:KNOWS]->(s:Skill)
    RETURN r.uid AS rid, c.uid AS cid, c.name AS name, c.email AS email, 
           s.uid AS sid, s.name AS skill, s.category AS category
    """

    conn = Neo4jConnection()
    result = conn.query(query)
    data = pd.DataFrame([dict(record) for record in result])
    data.to_csv(OUTPUT_FILE, index=False)
    conn.close()


if __name__ == "__main__":
    export_from_neo4j()
