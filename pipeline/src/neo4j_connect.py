from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        
    def close(self):
        self.driver.close()
        
    def query(self, query, parameters=None):
        with self.driver.session() as session:
            response = list(session.run(query, parameters))
            return response