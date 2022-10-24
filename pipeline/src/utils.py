INPUT_PATH = 'pipeline/src/input/Zifo Europe - Skills Survey(1-77).csv'
OUTPUT_PATH = 'pipeline/src/input/neo4jimport.csv'

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

class CategoryColumnMap:
    map = {
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