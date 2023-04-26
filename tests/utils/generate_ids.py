import uuid

import pandas as pd


def main():
    """
    Add 3 unique uuid fields to mock_skills_data.csv.
    How to use: copy mock_skills_data.csv into utils folder, execute generate_ids.py, new file
    mock_skills_data_out.csv is generated with 3 unique integer ID fields.

    description of IDs:
    rid: relationship id
    cid: consultant id
    sid: skill id
    """
    df = pd.read_csv("mock_skills_data.csv")
    df.insert(0, "rid", pd.Series([uuid.uuid4() for _ in df.index]))

    consultants_df = pd.DataFrame(df.name.unique())
    consultants_df.insert(
        0, "cid", pd.Series([uuid.uuid4() for _ in consultants_df.index])
    )
    print(consultants_df)
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

    df.to_csv("mock_skills_data_out.csv", index=False)


if __name__ == "__main__":
    main()
