from neo4j import GraphDatabase
import time

from prepare import category_column_map

"""
https://colab.research.google.com/drive/1J9__HotNoINHpucoipLH-4qWc48GALAk?usp=sharing#scrollTo=whSNmJ2OEfLM
Most code below from above link
"""

"""
https://neo4j.com/developer/docker-run-neo4j/
Execute below command to run neo4j container

docker run \
    --name testneo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
    --env NEO4JLABS_PLUGINS='["apoc"]' \
    neo4j:latest
"""

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def query(self, query, parameters=None):
        with self.driver.session() as session:
            response = list(session.run(query, parameters))
            return response

def add_skills(conn, data, category):
    # query = (f'''UNWIND $rows AS row
    # FOREACH (x IN CASE WHEN row.'''
    # + category
    # + ''' IS NULL THEN [] ELSE [1] END |

    # '''
    # f"MERGE (:{category}"
    # + "{Name: row."
    # + category
    # + '''})
    # RETURN count(*) as total
    # '''
    #)

    query = """UNWIND $rows AS row
    MERGE (c:Name{Name: row.Name, email: row.Email, id:row.ID})
    FOREACH(x IN CASE WHEN row.Service IS NOT NULL THEN [1] END |
    MERGE (sa:Service{Name: row.Service})
    """

    # FOREACH(x IN CASE WHEN row.Service IS NOT NULL THEN [1] END |
    # MERGE (sa:Service{Name: row.Service})
    # MERGE (c)-[:KNOWS]->(sa)"""

    return insert_data(conn, query, data)

def add_people(conn, rows, categories, batch_size=5000):
    # Adds paper nodes and (:Author)--(:Paper) and (:Paper)--(:Category)
    # relationships to the Neo4j graph as a batch job.  (Note the smaller batch
    # size due to the fact that this function is adding much more data than the
    # add_authors() function.)

    query = '''
    UNWIND $rows as row
    MERGE (n:Name {id:row.ID}) ON CREATE SET n.Name = row.Name
    '''

    # for category in categories:
    #     query = (
    #         query + 
    #     '''

    #     WITH row, n
    #     UNWIND row.'''
    #     + category
    #     + ''' AS value
    #     MATCH (c:'''
    #     + category
    #     + ''' {Name: value})
    #     MERGE (n)-[:KNOWS]->(c)
    #     '''
    #     )

    query = query + (
        """
        
        RETURN count(distinct n) as total
        """
    )

    return insert_data(conn, query, rows, batch_size)

def insert_data(conn, query, data, batch_size = 10000):
    # Function to handle the updating the Neo4j database in batch mode.

    total = 0
    batch = 0
    start = time.time()
    result = None

    while batch * batch_size < len(data):

        import pprint
        print(len(data))

        pprint.pprint(len(data[batch * batch_size: (batch + 1) * batch_size].dropna().to_dict('records')))
        res = conn.query(query, parameters={'rows': data[batch * batch_size: (batch + 1) * batch_size].to_dict('records')})
        print(res)
        total += res[0]['total']
        batch += 1
        result = {"total":total, "batches":batch, "time":time.time()-start}
        print(result)

    return result

def create_category_constraints(conn):
    for category in category_column_map:
        conn.query(f'CREATE CONSTRAINT ON (c:{category}) ASSERT c.Name IS UNIQUE')
