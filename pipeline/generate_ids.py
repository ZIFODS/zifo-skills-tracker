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
    df.insert(0, "rid", pd.Series([uuid.uuid4() for _ in df.index]))

    consultants_df = pd.DataFrame(df.name.unique())
    consultants_df.insert(
        0, "cid", pd.Series([uuid.uuid4() for _ in consultants_df.index])
    )

    df.insert(
        1,
        "cid",
        pd.Series(
            [
                consultants_df.loc[consultants_df[0] == name, "cid"].values[0]
                for name in df["name"].to_list()
            ]
        ),
    )

    skills_df = pd.DataFrame(df.skill.unique())
    skills_df.insert(0, "sid", pd.Series([uuid.uuid4() for _ in skills_df.index]))

    df.insert(
        4,
        "sid",
        pd.Series(
            [
                skills_df.loc[skills_df[0] == skill, "sid"].values[0]
                for skill in df["skill"].to_list()
            ]
        ),
    )

    return df
