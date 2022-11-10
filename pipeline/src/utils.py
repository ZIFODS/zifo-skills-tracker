from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../../").resolve()
sys.path.append(str(root_dir))

from enum import Enum

INPUT_PATH = f'{root_dir}/pipeline/input/Zifo Europe - Skills Survey(1-77).csv'
OUTPUT_PATH = f'{root_dir}/pipeline/import/neo4jimport.csv'

class Identifiers(Enum):
    ID = "Id"
    FULL_NAME = "Full_name"
    EMAIL = "Email"

class Categories(Enum):
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