from database import Neo4jConnection, add_people, add_skills, create_category_constraints
from prepare import category_column_map, get_unique_skills_for_category, load_data, skills_nodes_to_lists

def main():
    data = load_data()
    data = skills_nodes_to_lists(data)
    unique_skills = {category: get_unique_skills_for_category(data, category) for category in category_column_map}

    conn = Neo4jConnection(uri="neo4j://localhost:7687", user="neo4j", pwd="test")

    conn.query("MATCH (n) DETACH DELETE n;")
    conn.query("CALL apoc.schema.assert({}, {})")

    conn.query(f'CREATE CONSTRAINT ON (n:Name) ASSERT n.Name IS UNIQUE')
    create_category_constraints(conn)

    for category_name, category_data in unique_skills.items():
        add_skills(conn, category_data, category_name)

    add_people(conn, data, list(unique_skills.keys()))

    conn.close()

if __name__ == "__main__":
    main()
