import uuid

import pandas as pd


def generate_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add 3 unique UUID fields to skills data for import into neo4j.

    description of IDs:
    rid: relationship id
    cid: consultant id
    sid: skill id

    Parameters
    ----------
    df : pd.DataFrame
        skills data for consultants

    Returns
    -------
    df : pd.DataFrame
        skills data for consultants with UUIDs for each node/relationship.
    """
    # Ensure consistent index
    df = df.reset_index(drop=True)

    # Unique relationship ID per row
    df.insert(0, "rid", pd.Series([str(uuid.uuid4()) for _ in df.index]))

    # Consultant ID based on name
    unique_names = df["name"].unique()
    name_to_cid = {name: str(uuid.uuid4()) for name in unique_names}
    df.insert(1, "cid", df["name"].map(name_to_cid))

    # Skill ID based on skill name
    unique_skills = df["skill"].unique()
    skill_to_sid = {skill: str(uuid.uuid4()) for skill in unique_skills}
    df.insert(4, "sid", df["skill"].map(skill_to_sid))

    return df
