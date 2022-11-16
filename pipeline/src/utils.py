'''
Global variables representing values in the input and output CSVs.
'''
from pathlib import Path
import sys
import re
import os
from enum import Enum
root_dir = (Path(__file__).parent / "../../").resolve()
sys.path.append(str(root_dir))

# Acquire the local path to Zifo Skills Survey csv
try:
    skills_csv_pattern = "Zifo Europe - Skills Survey.*\.csv"
    skills_csv = [
            file for file in os.listdir(f'{root_dir}/pipeline/input/') 
            if re.search(pattern=skills_csv_pattern, string=file)
        ][0]
    INPUT_PATH = f'{root_dir}/pipeline/input/{skills_csv}'
except IndexError:
    raise IndexError("Could not locate the Skills Survey CSV in pipeline/input directory")
    
OUTPUT_PATH = f'{root_dir}/pipeline/import/neo4jimport.csv'


class Identifiers(Enum):
    '''
    ID realted values.
    '''
    ID = "Id"
    FULL_NAME = "Full_name"
    EMAIL = "Email"

class Categories(Enum):
    '''
    New column values for output csv file.
    '''
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

class ColumnHeaderMap:
    '''
    Original column values from survey export.
    '''
    map = {
        Identifiers.ID.value: "ID",
        Identifiers.FULL_NAME.value: "Name",
        Identifiers.EMAIL.value: "Email",
        Categories.SERVICE.value: "Please tick all Service elements that you feel you have a reasonable knowledge of",
        Categories.METHODOLOGY.value: "Please tick all Methodologies that you feel you have a reasonable knowledge of",
        Categories.SCI_PRODUCT_APP.value: "Please tick all Scientific Products & Applications that you feel you have a reasonable knowledge of",
        Categories.RESEARCH_DEV.value: "Please tick all R&D Processes that you feel you have a reasonable knowledge of",
        Categories.PRODUCT_APP.value: "Please tick all Products & Applications that you feel you have a reasonable knowledge of",
        Categories.REGULATION.value: "Please tick all Regulations that you feel you have a reasonable knowledge of",
        Categories.DATA_MANAGEMENT.value: "Please tick all Data Management skills that you feel you have a reasonable knowledge of",
        Categories.LANGUAGE.value: "Please tick all Languages that you feel you have a reasonable knowledge of",
        Categories.PROGRAMMING.value: "Please tick all Programming Languages that you feel you have a reasonable knowledge of",
        Categories.MISCELLANEOUS.value: "Please tick all that you feel you have reasonable knowledge of",
        Categories.INFRASTRUCTURE.value: "Please tick all Infrastructure Technologies that you feel you have a reasonable knowledge of"
    }
