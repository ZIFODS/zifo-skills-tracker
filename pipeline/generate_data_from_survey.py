import pandas as pd
import numpy as np
from pipeline.schemas import ColumnHeaderMap, Columns, Categories

INPUT_PATH = "skills-survey-export.xlsx"
OUTPUT_PATH = "neo4j-import.csv"


def main():
    generate_from_survey()


def generate_from_survey():
    """
    Convert data from MS Forms survey export to neo4j import format.
    """
    all_data = pd.read_excel(INPUT_PATH)
    all_data = all_data.rename({v: k for k, v in ColumnHeaderMap.map.items()}, axis=1)

    name_data = all_data[
        [Columns.ID.value, Columns.NAME.value, Columns.EMAIL.value]
    ]
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

    # write to csv
    melted_df.to_csv(OUTPUT_PATH, index=False)


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


if __name__ == "__main__":
    main()
