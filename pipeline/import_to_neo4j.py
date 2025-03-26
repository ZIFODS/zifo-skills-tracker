import sys
import uuid
from pathlib import Path

import pandas as pd
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from app.utils.neo4j_connect import Neo4jConnection  # noqa: E402
from app.config import NEO4J_URI  # noqa: E402

INPUT_FILE = "backup.csv"

CONSTRAINTS = [
    "CREATE CONSTRAINT consultant_email_unique IF NOT EXISTS FOR (n:Consultant) REQUIRE n.email IS UNIQUE",
    "CREATE CONSTRAINT skill_name_unique IF NOT EXISTS FOR (n:Skill) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT consultant_uid_unique IF NOT EXISTS FOR (n:Consultant) REQUIRE n.uid IS UNIQUE",
    "CREATE CONSTRAINT skill_uid_unique IF NOT EXISTS FOR (n:Skill) REQUIRE n.uid IS UNIQUE",
    "CREATE CONSTRAINT knows_uid_unique IF NOT EXISTS FOR ()-[r:KNOWS]-() REQUIRE r.uid IS UNIQUE"
]


def import_from_file(file: str):
    df = pd.read_csv(file)
    print(f"Establishing connection to Neo4J DB: {NEO4J_URI}")
    input_str = input("Write data to this DB (only 'yes' accepted)? ")
    if not input_str == "yes":
        print("Aborted by user")
        return
    input_str = input("Generate new relation IDs? (only 'yes' accepted - defaults to no) ")
    generate_rids = input_str != "yes"
    conn = Neo4jConnection()

    with conn.driver.session() as session:
        for constraint in CONSTRAINTS:
            session.run(constraint)

        for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
            rid = str(uuid.uuid4()) if generate_rids else row['rid']
            session.write_transaction(
                create_or_update_nodes_and_relationships,
                consultant_id=row['cid'],
                name=row['name'],
                email=row['email'],
                skill_id=row['sid'],
                skill=row['skill'],
                category=row['category'],
                relation_id=rid
            )
    conn.close()


def create_or_update_nodes_and_relationships(tx, consultant_id, name, email, skill_id, skill, category, relation_id):
    a = tx.run("""
           MERGE (c:Consultant {email: $email})
           ON CREATE SET c.name = $name, c.uid = $consultant_id

           MERGE (s:Skill {uid: $skill_id})
           ON CREATE SET s.name = $skill, s.category = $category

           MERGE (c)-[r:KNOWS]->(s)
           ON CREATE SET r.uid = $rel_id;
       """, consultant_id=consultant_id, name=name, email=email, skill_id=skill_id, skill=skill, category=category,
               rel_id=relation_id)

    # Consume result to check for warnings
    summary = a.consume()
    if summary.notifications:
        for notification in summary.notifications:
            print("Warning:", notification["title"])
            print("Description:", notification["description"])
            print("Severity:", notification["severity"])


if __name__ == "__main__":
    import_from_file(INPUT_FILE)
