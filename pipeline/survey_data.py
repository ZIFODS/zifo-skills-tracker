import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from app.utils.neo4j_connect import Neo4jConnection  # noqa: E402
from pipeline.generate_ids import generate_ids  # noqa: E402
from pipeline.schemas import Categories, ColumnHeaderMap, Columns  # noqa: E402

INPUT_PATH = "data/skills-survey-export.xlsx"
OUTPUT_PATH = "data/prod_skills_data.csv"


class MultipleSkillsFoundError(Exception):
    pass


def main():
    df = generate_from_survey()
    df = generate_ids(df)
    df = update_skills_ids(df)
    df.to_csv(OUTPUT_PATH, index=False)


def generate_from_survey():
    """
    Convert data from MS Forms survey export to neo4j import format.
    """
    all_data = pd.read_excel(INPUT_PATH)
    all_data = all_data.rename({v: k for k, v in ColumnHeaderMap.map.items()}, axis=1)

    name_data = all_data[[Columns.ID.value, Columns.NAME.value, Columns.EMAIL.value]]
    skill_data = all_data[[i.value for i in Categories]]

    # Split strings by semi-colon and convert nan to empty list
    skill_data = skill_data.apply(lambda x: split_strings(x))
    skill_data = skill_data.apply(lambda x: x.fillna({i: [] for i in x.index}))
    # Get maximum list length on each row
    skill_data["max_length"] = skill_data.apply(lambda x: x.map(len).max(), axis=1)

    # Extend all lists on each row to max length
    skill_data = skill_data.apply(
        lambda x: x.iloc[:-1].apply(lambda y: extend_list(y, x["max_length"])), axis=1
    )

    # Explode columns individually to keep one skill per row
    skill_data_sep = pd.DataFrame()
    for col in Categories:
        col_sep = skill_data[col.value].explode().to_frame()
        skill_data_sep = pd.concat([skill_data_sep, col_sep])

    # Remove full nan rows
    skill_data_sep = skill_data_sep.replace("", np.nan)
    skill_data_sep = skill_data_sep.dropna(how="all")

    df = name_data.join(skill_data_sep)

    # melt dataframe to convert from wide to long format
    melted_df = pd.melt(
        df,
        id_vars=[Columns.NAME.value, Columns.EMAIL.value, Columns.ID.value],
        var_name=Columns.CATEGORY.value,
        value_name=Columns.SKILL.value,
    )

    # remove row where skill column value is NaN
    melted_df = melted_df.dropna(subset=[Columns.SKILL.value])

    # sort df by Id column, drop Id column, then reset index
    melted_df = (
        melted_df.sort_values(by=[Columns.ID.value])
        .drop(labels=Columns.ID.value, axis=1)
        .reset_index(drop=True)
    )

    melted_df = melted_df[
        [
            Columns.NAME.value,
            Columns.EMAIL.value,
            Columns.SKILL.value,
            Columns.CATEGORY.value,
        ]
    ]

    # convert strings in email column to lowercase
    melted_df[Columns.EMAIL.value] = melted_df[Columns.EMAIL.value].str.lower()

    return melted_df


def split_strings(input):
    """
    Splits the strings by semicolon
    Arguments
    ------------
    input : str - item in the list
    """
    return input.str.split(";")


def extend_list(list_value, max_length):
    """
    Extends the list to be length of the list in the series with the highest length
    Arguments
    ----------
    list_value : list - items from the list
    max_length : int - length of the longest list
    Returns
    ---------
    list_value : list
    """
    list_value.extend([np.nan for _ in range(max_length - len(list_value))])
    return list_value


def update_skills_ids(survey_df: pd.DataFrame) -> pd.DataFrame:
    """
    Update skill ID with existing value if skill name already exists in neo4j.

    Parameters
    ----------
    survey_df : pd.DataFrame
        dataframe with consultant - skill relationship on each row
        IDs for skills must already be added

    Returns
    -------
    survey_df : pd.DataFrame
        dataframe with IDs updated for skills that already exist
    """
    conn = Neo4jConnection()
    survey_df["sid"] = survey_df.apply(
        lambda x: get_skill_id_from_name(conn, x["skill"], x["sid"]), axis=1
    )
    conn.close()
    return survey_df


def get_skill_id_from_name(
    conn: Neo4jConnection, skill_name: str, skill_id: str
) -> str:
    """
    Given a skills name, get the ID of that skill from neo4j.
    If it doesn't exist, use the new skill ID that is already in the dataframe.

    Parameters
    ----------
    conn : Neo4jConnection
        connection to neo4j database
    skill_name : str
        name of skill
    skill_id : str
        new skill ID assigned if skill doesn't exist

    Returns
    -------
    str
        id of skill to be used

    Raises
    ------
    MultipleSkillsFoundError
        If multiple skills with same name are found in neo4j
    """
    result = conn.query("MATCH (s:Skill {name: $name}) RETURN s.uid", name=skill_name)
    if len(result) == 0:
        return skill_id
    if len(result) == 1:
        return result[0][0]
    else:
        raise MultipleSkillsFoundError(
            f"Multiple skills were found with name {skill_name}"
        )


if __name__ == "__main__":
    main()
