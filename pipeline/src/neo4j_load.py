from neo4j_connect import Neo4jConnection


def get_cypher_queries():
    with open("pipeline/src/cypher_load.txt") as file:
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

def load_neo4j():
    queries = get_cypher_queries()

    conn = Neo4jConnection(uri="neo4j://localhost:7687", user="neo4j", password="test")

    for query in queries:
        conn.query(query)

    conn.close()

if __name__ == "__main__":
    load_neo4j()