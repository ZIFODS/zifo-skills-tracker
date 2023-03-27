import random

import pandas as pd

mock_consultants = [
    "Anthony Hopkins",
    "Catherine Zeta-Jones",
    "Michael Sheen",
    "Tom Jones",
    "Ioan Gruffudd",
    "Matthew Rhys",
    "Gareth Bale",
    "Ryan Giggs",
    "Charlotte Church",
    "Rob Brydon",
    "Ruth Jones",
    "Duffy",
    "Glynis Johns",
    "Ray Milland",
    "Bonnie Tyler",
    "Bryn Terfel",
    "Shirley Bassey",
    "Richard Burton",
    "Sian Phillips",
    "Cerys Matthews",
    "Max Boyce",
    "Derek Brockway",
    "Nerys Hughes",
    "Taron Egerton",
    "Katherine Jenkins",
    "Iwan Rheon",
    "Alex Jones",
    "Colin Jackson",
    "Ellie Goulding",
    "Gethin Jones",
    "John Cale",
    "Geraint Thomas",
    "Christian Bale",
    "Tom Ellis",
    "Alun Wyn Jones",
    "Ryan Davies",
    "Owain Yeoman",
    "Budgie",
    "David Emanuel",
    "Tanni Grey-Thompson",
    "Adam Price",
    "Huw Edwards",
    "Aled Jones",
    "Leigh Halfpenny",
    "Rhod Gilbert",
    "Gwyneth Powell",
    "Kiri Te Kanawa",
    "Nigel Owens",
    "Sian Lloyd",
    "Gareth Thomas",
    "Rob Howley",
    "Bryn Parry-Jones",
]

MIN_SKILLS = 10
MAX_SKILLS = 20
MAX_SKILLS_PER_CATEGORY = 5


def main():
    skills = load_skills()
    df = assign_skills(skills)
    df.to_csv("mock_data.csv", index=False)


def load_skills():
    skill_df = pd.read_csv("../skills-list.csv")
    return skill_df


def get_categories(skill_df: pd.DataFrame) -> list[str]:
    categories = skill_df["Category"].unique()
    return list(categories)


def assign_skills(skill_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign skills to mock consultants. Each consultant will have a random number of
    skills assigned to them within each category. The total number of skills assigned
    to each consultant should fall within the range MIN_SKILLS and MAX_SKILLS.

    Parameters
    ----------
    skill_df : pd.DataFrame
        Dataframe containing skills and categories

    Returns
    -------
    pd.DataFrame
        Dataframe containing mock consultant name, email, and a skill and category
        per row
    """
    categories = get_categories(skill_df)
    columns = ["name", "email", "skill", "category"]
    df = pd.DataFrame(columns=columns)

    for consultant in mock_consultants:
        consultant_df = pd.DataFrame(columns=columns)
        category_skill_numbers = generate_category_skill_numbers(categories)

        for category in categories:
            category_skills = skill_df[skill_df["Category"] == category].sample(
                n=category_skill_numbers[category]
            )
            for _, sampled_skill in category_skills.iterrows():
                row = {
                    "name": [consultant],
                    "email": [consultant.replace(" ", "_").lower() + "@gmail.com"],
                }
                row["skill"] = [sampled_skill["Skill"]]
                row["category"] = [sampled_skill["Category"]]
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
