import pandas as pd
import numpy as np

class Categories:
    SERVICE = "Service"
    METHODOLOGY = "Methodology"
    SCI_PRODUCT_APP = "Scientific_Products_And_Applications"
    RESEARCH_DEV = "R_And_D_Processes"
    PRODUCT_APP = "Products_And_Applications"
    REGULATION = "Regulation"
    DATA_MANAGEMENT = "Data_Management"
    LANGUAGE = "Languages"
    PROGRAMMING = "Programming_languages"
    MISCELLANEOUS = "Miscellaneous"
    INFRASTRUCTURE = "Infrastructure_Technologies"

category_column_map = {
    Categories.SERVICE: "Please tick all Service elements that you feel you have a reasonable knowledge of",
    Categories.METHODOLOGY: "Please tick all Methodologies that you feel you have a reasonable knowledge of",
    Categories.SCI_PRODUCT_APP: "Please tick all Scientific Products & Applications that you feel you have a reasonable knowledge of",
    Categories.RESEARCH_DEV: "Please tick all R&D Processes that you feel you have a reasonable knowledge of",
    Categories.PRODUCT_APP: "Please tick all Products & Applications that you feel you have a reasonable knowledge of",
    Categories.REGULATION: "Please tick all Regulations that you feel you have a reasonable knowledge of",
    Categories.DATA_MANAGEMENT: "Please tick all Data Management skills that you feel you have a reasonable knowledge of",
    Categories.LANGUAGE: "Please tick all Languages that you feel you have a reasonable knowledge of",
    Categories.PROGRAMMING: "Please tick all Programming Languages that you feel you have a reasonable knowledge of",
    Categories.MISCELLANEOUS: "Please tick all that you feel you have reasonable knowledge of",
    Categories.INFRASTRUCTURE: "Please tick all Infrastructure Technologies that you feel you have a reasonable knowledge of"
}

def load_data():
    return pd.read_csv("pipeline/src/Zifo Europe - Skills Survey(1-77).csv")
    

def skills_nodes_to_lists(data: pd.DataFrame):
    for column in category_column_map.values():
        data[column] = data[column].str.split(";")

    reverse_map = {v: k for k, v in category_column_map.items()}

    data = data.rename(columns=reverse_map)
    data = data.replace(r'^\s*$', np.nan, regex=True)

    return data

def get_unique_skills_for_category(data, category):
    df_column = (
        pd.DataFrame(data[[category]])
            .explode(category)
            .drop_duplicates(subset=[category])
    )
    return df_column
