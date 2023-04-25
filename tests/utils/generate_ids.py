import pandas as pd


def main():
    """
    Add 3 unique integer ID fields to mock_skills_data.csv.
    How to use: copy mock_skills_data.csv into utils folder, execute generate_ids.py, new file
    mock_skills_data_out.csv is generated with 3 unique integer ID fields.

    description of IDs:
    rid (0 to number of links - 1): relationship id
    cid (max rid + 1 to max rid + number of consultants): consultant id
    sid (max cid + 1 to max cid + number of skills): skill id
    """
    df = pd.read_csv("mock_skills_data.csv")
    df.insert(0, "rid", pd.Series(list(range(len(df)))))

    consultants_df = pd.Series(df.name.unique())
    skills_df = pd.Series(df.skill.unique())

    df.insert(
        1,
        "cid",
        pd.Series(
            [
                consultants_df.index[consultants_df == name].values[0] + len(df)
                for name in df["name"].to_list()
            ]
        ),
    )
    df.insert(
        4,
        "sid",
        pd.Series(
            [
                skills_df.index[skills_df == skill].values[0]
                + len(df)
                + len(consultants_df)
                for skill in df["skill"].to_list()
            ]
        ),
    )

    df.to_csv("mock_skills_data_out.csv", index=False)


if __name__ == "__main__":
    main()
