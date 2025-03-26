import pandas as pd
from tqdm import tqdm

from get_prima_data import get_bearer_token, get_data_with_token
from generate_ids import generate_ids
from app.utils.neo4j_connect import Neo4jConnection  # noqa: E402

CATEGORY_KEY_MAPPING = {
    "Data Management": "Data_Management",
    "Infrastructure": "Infrastructure_Technologies",
    "Languages": "Languages",
    "Methodologies": "Methodology",
    "Products & Applications": "Products_And_Applications",
    "Programming Languages and Libraries & Frameworks": "Programming_languages",
    "R&D Processes": "R_And_D_Processes",
    "Regulations": "Regulation",
    "Scientific Products & Applications": "Scientific_Products_And_Applications",
    "Services": "Service"
}


def process_skills_data(api_response: dict, allowed_regions: list, output_path: str = "skills_data.csv") -> pd.DataFrame:
    import pandas as pd

    # Extract and convert to DataFrame
    data = api_response.get("data", [])
    df = pd.DataFrame(data)

    # Filter by region
    df = df[df["region"].isin(allowed_regions)]

    # Rename columns to match what generate_ids expects
    df.rename(columns={
        "emp_name": "name",
        "skill_name": "skill",
        "work_email": "email",
        "skill_type": "category"
    }, inplace=True)

    # Only keep relevant columns for import
    df = df[["name", "skill", "email", "category"]]

    # Generate UUIDs using the existing function
    df = generate_ids(df)

    # Reorder columns to match Neo4j load order (optional)
    df = df[["rid", "cid", "name", "email", "sid", "skill", "category"]]

    # Save to CSV
    df.to_csv(output_path, index=False)

    return df


def import_skills_df_to_neo4j(df, reset_db: bool = True):
    """
    Imports skills data from a DataFrame into Neo4j using parameterized Cypher.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns: rid, cid, name, email, sid, skill, category
    reset_db : bool
        If True, clears the existing graph and recreates constraints.
    """
    conn = Neo4jConnection()

    try:
        if reset_db:
            print("⚠️ Resetting database and applying constraints...")
            setup_queries = [
                "MATCH (n) DETACH DELETE n",
                "CALL apoc.schema.assert({},{},true) YIELD label, key RETURN *",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Consultant) REQUIRE c.email IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Consultant) REQUIRE c.uid IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Skill) REQUIRE s.uid IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR ()-[r:KNOWS]-() REQUIRE r.uid IS UNIQUE",
            ]
            for q in setup_queries:
                conn.query(q)

        print("🚀 Importing rows into Neo4j...")
        query = """
        MERGE (c:Consultant {uid: $cid})
        SET c.name = $name, c.email = $email

        MERGE (s:Skill {uid: $sid})
        SET s.name = $skill, s.category = $category

        MERGE (c)-[:KNOWS {uid: $rid}]->(s)
        """

        # Ensure UUIDs are strings
        uuid_cols = ["rid", "cid", "sid"]
        df[uuid_cols] = df[uuid_cols].astype(str)

        # Add tqdm progress bar
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Importing to Neo4j"):
            try:
                conn.query(query,
                           cid=row["cid"],
                           name=row["name"],
                           email=row["email"],
                           sid=row["sid"],
                           skill=row["skill"],
                           category=CATEGORY_KEY_MAPPING[row["category"]],
                           rid=row["rid"]
                           )
            except Exception as e:
                print(f"❌ Error on row {idx + 1}: {e}")
                print(f"   Row data: {row.to_dict()}")
                raise  # Reraise to stop if needed

        print("✅ DataFrame successfully imported to Neo4j.")

    except Exception as e:
        print(f"❌ Fatal error during Neo4j import: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    filename = f"skills_data_prima.csv"
    token = get_bearer_token()
    api_data = get_data_with_token(token)
    new_df = process_skills_data(api_data, ["Europe"], filename)
    import_skills_df_to_neo4j(new_df)
