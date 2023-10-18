"""
Establishes Neo4j connection
"""
from neo4j import GraphDatabase

from app.config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER


class Neo4jConnection:
    """
    Class for initiating Neo4j session.
    """

    def __init__(
        self,
        uri: str = NEO4J_URI,
        user: str = NEO4J_USER,
        password: str = NEO4J_PASSWORD,
    ):
        """
        Init method
        Arguments
        ----------
        uri : str
        user : str
        password: str
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Closes Driver
        """
        self.driver.close()

    def query(self, query, **kwargs):
        """
        Makes query for initating session
        Arguments
        ----------
        query : query

        Returns
        ----------
        response : list
        """
        with self.driver.session() as session:
            response = list(session.run(query, **kwargs))
            return response
