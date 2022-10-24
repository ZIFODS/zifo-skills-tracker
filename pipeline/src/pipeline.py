import pandas as pd
import numpy as np

from pipeline.src.neo4j_load import load_neo4j
from pipeline.src.utils import INPUT_PATH, OUTPUT_PATH, CategoryColumnMap

def main():
    load_data()
    load_neo4j()

def load_data():

    all_data = pd.read_csv(INPUT_PATH, header=0)
    all_data = all_data.rename({v: k for k, v in CategoryColumnMap.map.items()})

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
    for col in CategoryColumnMap.map:
        col_sep = skill_data[col].explode().to_frame()
        skill_data_sep = pd.concat([skill_data_sep, col_sep])

    # Remove full nan rows
    skill_data_sep = skill_data_sep.dropna(how="all")

    output_data = name_data.join(skill_data_sep)

    output_data.to_csv(OUTPUT_PATH, index=False)

def split_strings(input):
    return input.str.split(';')

def extend_list(list_value, max_length):
    list_value.extend([np.nan for _ in range(max_length - len(list_value))])
    return list_value

if __name__ == "__main__":
    main()
