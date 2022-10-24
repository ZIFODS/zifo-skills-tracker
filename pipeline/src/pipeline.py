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

def main():

    neo4J_input_file = 'Zifo Europe - Skills Survey(1-77).csv'
    neo4J_input_path = 'pipeline/src/input/' + neo4J_input_file

    load_data(neo4J_input_path)

def load_data(path):

    all_data = pd.read_csv(path, header=0)
    all_data = all_data.rename({v: k for k, v in all_data.items()})

    name_data = all_data[["ID", "Name", "Email"]]
    
    skill_data = all_data.drop(['ID','Start time','Completion time', "Name", "Email"], axis=1)

    # Split strings by semi-colon and convert nan to empty list
    skill_data = skill_data.apply(lambda x: split_strings(x))  
    skill_data = skill_data.apply(lambda x: x.fillna({i: [] for i in x.index}))

    # Get maximum list length on each row
    skill_data["max_length"] = skill_data.apply(lambda x: x.map(len).max(), axis=1)

    # Extend all lists on each row to max length
    skill_data = skill_data.apply(lambda x: x.iloc[:-1].apply(lambda y: extend_list(y, x["max_length"])), axis=1)

    # Explode columns individually to keep one skill per row
    skill_data_sep = pd.DataFrame()
    for col in category_column_map:
        col_sep = skill_data[col].explode().to_frame()
        skill_data_sep = pd.concat([skill_data_sep, col_sep])

    # Remove full nan rows
    skill_data_sep = skill_data_sep.dropna(how="all")

    output_data = name_data.join(skill_data_sep)

    output_path = 'pipeline/src/input/neo4jimport.csv'
    output_data.to_csv(output_path, index=False)

def split_strings(input):
    return input.str.split(';')

def extend_list(list_value, max_length):
    list_value.extend([np.nan for _ in range(max_length - len(list_value))])
    return list_value

main()
