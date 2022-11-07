from neo4j_connect import Neo4jConnection
from pipeline.src.utils import OUTPUT_PATH


def get_cypher_queries():
    with open(OUTPUT_PATH) as file:
        cypher = file.readlines()

        queries = []
        query = ""
        for line in cypher:

            if line.startswith("CREATE") or line.startswith("MATCH") or line.startswith("CALL"):
                queries.append(line)

            elif not line.startswith("-") or not line.strip():
                query += line

        queries.append(query)
        
        queries.pop(0)

        return queries

columns = [
    "science_apps",
    "services",
    "methodologies",
    "process",
    "other_products",
    "regulatory",
    "data_management",
    "languages",
    "programming",
    "misc",
    "infrastructure"
]

def new_get_cypher_queries():
    queries = [
    "CREATE CONSTRAINT ON (c:Consultant) ASSERT c.Name IS UNIQUE",
    "CREATE CONSTRAINT ON (s:Skill) ASSERT s.Name IS UNIQUE",

    "CREATE INDEX ON :Consultant(name)",
    "CREATE INDEX ON :Skill(name)",
    ]

    query = """
    LOAD CSV WITH HEADERS FROM 'file:///neo4jimport.csv' AS row
    MERGE (c:Consultant{Name: row.fullname, email: row.email, id:row.id})
    """

    for col in columns:
        query += f"""
        FOREACH(x IN CASE WHEN row.{col} IS NOT NULL THEN [1] END |
        MERGE (s: Skill """
        query += "{Name: row."
        query += f'{col}, Group: "{col}"'
        query += """})
        MERGE (c)-[:KNOWS]->(mi))
        """
        
    queries.append(query)
    
    return queries

def load_neo4j():
    queries = get_cypher_queries()

    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    for query in queries:
        conn.query(query)

    conn.close()

if __name__ == "__main__":
    load_neo4j()