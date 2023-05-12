import json
import random
import sys
from pathlib import Path
from typing import Tuple

import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from pipeline.generate_ids import generate_ids  # noqa: E402
from pipeline.schemas import Columns  # noqa: E402

MIN_SKILLS = 10
MAX_SKILLS = 20
MAX_SKILLS_PER_CATEGORY = 5

INPUT_PATH = "pipeline/mock_seed.json"
OUTPUT_PATH = "data/mock_skills_data.csv"


def main():
    consultants, skills = extract_seed_data()
    df = assign_skills(consultants, skills)
    df = generate_ids(df)
    df.to_csv(OUTPUT_PATH, index=False)


def get_categories(skill_df: pd.DataFrame) -> list[str]:
    categories = skill_df[Columns.CATEGORY.value].unique()
    return list(categories)


def extract_seed_data() -> Tuple[list[str], pd.DataFrame]:
    """
    Extract mock consultants and skills from the mock_seed.json file.

    Returns
    -------
    consultants: list[str]
        List of mock consultant names
    skill_df: pd.DataFrame
        Dataframe with skill-category pair on each row
    """
    with open(INPUT_PATH, "r") as f:
        data = json.load(f)

    consultants = data["consultants"]

    skills = data["skills"]
    skill_df = pd.DataFrame.from_dict(skills, orient="index").transpose()
    skill_df = pd.melt(
        skill_df.reset_index(),
        id_vars=["index"],
        value_vars=skill_df.columns,
        var_name="category",
        value_name="skill",
    )
    skill_df = skill_df.dropna(subset=["skill"]).reset_index(drop=True)
    skill_df = skill_df.drop(columns=["index"])

    return consultants, skill_df


def assign_skills(consultants: list[str], skill_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign skills to mock consultants. Each consultant will have a random number of
    skills assigned to them within each category. The total number of skills assigned
    to each consultant should fall within the range MIN_SKILLS and MAX_SKILLS.

    Parameters
    ----------
    consultants : list[str]
        List of mock consultant names
    skill_df : pd.DataFrame
        Dataframe with skill-category pair on each row

    Returns
    -------
    pd.DataFrame
        Dataframe containing mock consultant name, email, and a skill and category
        per row
    """
    categories = get_categories(skill_df)
    columns = [
        Columns.NAME.value,
        Columns.EMAIL.value,
        Columns.SKILL.value,
        Columns.CATEGORY.value,
    ]
    df = pd.DataFrame(columns=columns)

    for consultant in consultants:
        consultant_df = pd.DataFrame(columns=columns)
        category_skill_numbers = generate_category_skill_numbers(categories)

        for category in categories:
            category_skills = skill_df[
                skill_df[Columns.CATEGORY.value] == category
            ].sample(n=category_skill_numbers[category])

            for _, sampled_skill in category_skills.iterrows():
                row = {
                    Columns.NAME.value: [consultant],
                    Columns.EMAIL.value: [
                        consultant.replace(" ", "_").lower() + "@gmail.com"
                    ],
                }
                row[Columns.SKILL.value] = [sampled_skill[Columns.SKILL.value]]
                row[Columns.CATEGORY.value] = [sampled_skill[Columns.CATEGORY.value]]
                consultant_df = pd.concat(
                    [consultant_df, pd.DataFrame(row)], ignore_index=True
                )

        df = pd.concat([df, consultant_df], ignore_index=True)

    return df


def generate_category_skill_numbers(categories: list[str]) -> dict[str, int]:
    """
    Generate a dictionary of category: random number of skills that should be included
    for that category. The sum of the values in the dictionary should fall within the
    range MIN_SKILLS and MAX_SKILLS.

    Parameters
    ----------
    categories : list[str]
        List of categories to generate random numbers for.

    Returns
    -------
    dict[str, int]
        Dictionary of category: random number of skills for each category
    """
    categories_dict = {category: 0 for category in categories}

    # Generate random integers for each category until the sum falls within the range
    while True:
        # Reset the sum of integers to 0
        current_sum = 0

        # Loop through each category and assign a random integer between 1 and 10
        for category in categories_dict:
            value = random.randint(0, MAX_SKILLS_PER_CATEGORY)
            categories_dict[category] = value
            current_sum += value

        # Check if the sum of integers falls within the specified range
        if MIN_SKILLS <= current_sum <= MAX_SKILLS:
            break

    return categories_dict


if __name__ == "__main__":
    main()
