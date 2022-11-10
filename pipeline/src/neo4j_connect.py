'''
Establishes Neo4j connection
'''
from neo4j import GraphDatabase

class Neo4jConnection:
    '''
    Class for initiating Neo4j session.
    '''
    def __init__(self, uri, user, password):
        '''
        Init method
        Arguments
        ----------
        uri : str
        user : str
        password: str
        '''
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
    def close(self):
        '''
        Closes Driver
        '''
        self.driver.close()
    def query(self, query, parameters=None):
        '''
        Makes query for initating session
        Arguments
        ----------
        query : query
        parameters : None

        Returns
        ----------
        response : list
        '''
        with self.driver.session() as session:
            response = list(session.run(query, parameters))
            return response
