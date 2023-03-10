"""
Neo4j_Load
"""
from app.utils.neo4j_connect import Neo4jConnection
from pipeline.src.utils import Categories


def generate_cypher_queries():
    """
    Generating queries to sent to the service
    Returns
    -------
    queries : list[str]
    """
    queries = [
        "CREATE CONSTRAINT ON (c:Consultant) ASSERT c.Name IS UNIQUE",
        "CREATE CONSTRAINT ON (s:Skill) ASSERT s.Name IS UNIQUE",
        "CREATE INDEX ON :Consultant(name)",
        "CREATE INDEX ON :Skill(name)",
    ]

    query = """
    LOAD CSV WITH HEADERS FROM 'file:///neo4jimport.csv' AS row
    MERGE (c:Consultant {Name: row.Full_name, Group: 'Consultant', email: row.Email, id:row.Id})
    """

    for col in Categories:
        col_name = col.value
        query += f"""
        FOREACH(x IN CASE WHEN row.{col_name} IS NOT NULL THEN [1] END |
        MERGE (s: Skill """
        query += "{Name: row."
        query += f'{col_name}, Group: "{col_name}"'
        query += """})
        MERGE (c)-[:KNOWS]->(s))
        """
    queries.append(query)
    return queries


def load_neo4j():
    """
    Establishes a connection to the database.
    """
    queries = generate_cypher_queries()

    conn = Neo4jConnection()

    for query in queries:
        conn.query(query)

    conn.close()


if __name__ == "__main__":
    load_neo4j()
