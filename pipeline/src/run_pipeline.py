from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../../").resolve()
sys.path.append(str(root_dir))

import pandas as pd
import numpy as np

from pipeline.src.neo4j_load import load_neo4j
from pipeline.src.utils import INPUT_PATH, OUTPUT_PATH, ColumnHeaderMap, Identifiers, Categories

def main():
    load_data()
    load_neo4j()

def load_data():

    all_data = pd.read_csv(INPUT_PATH)
    all_data = all_data.rename({v: k for k, v in ColumnHeaderMap.map.items()}, axis=1)

    name_data = all_data[[Identifiers.ID.value, Identifiers.FULL_NAME.value, Identifiers.EMAIL.value]]
    
    skill_data = all_data.drop([Identifiers.ID.value,'Start time','Completion time', Identifiers.FULL_NAME.value, Identifiers.EMAIL.value], axis=1)

    # Split strings by semi-colon and convert nan to empty list
    skill_data = skill_data.apply(lambda x: split_strings(x))  
    skill_data = skill_data.apply(lambda x: x.fillna({i: [] for i in x.index}))

    # Get maximum list length on each row
    skill_data["max_length"] = skill_data.apply(lambda x: x.map(len).max(), axis=1)

    # Extend all lists on each row to max length
    skill_data = skill_data.apply(lambda x: x.iloc[:-1].apply(lambda y: extend_list(y, x["max_length"])), axis=1)

    # Explode columns individually to keep one skill per row
    skill_data_sep = pd.DataFrame()
    for col in Categories:
        col_sep = skill_data[col.value].explode().to_frame()
        skill_data_sep = pd.concat([skill_data_sep, col_sep])

    # Remove full nan rows
    skill_data_sep = skill_data_sep.replace("", np.nan)
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
