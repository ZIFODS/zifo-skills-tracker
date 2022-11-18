import os

from pipeline.src.utils import ROOT_DIR, EnviroVars, filter_survey_data, pull_survey_data_from_s3
os.makedirs(os.path.join(ROOT_DIR, str(EnviroVars.LOCAL_INPUT_DIR.value)), exist_ok=True)
OUTPUT_PATH = os.path.join(ROOT_DIR, str(EnviroVars.LOCAL_INPUT_DIR.value), "neo4jimport.csv")
INPUT_PATH = os.path.join(ROOT_DIR, str(EnviroVars.LOCAL_INPUT_DIR.value), "skills.csv")
filter_survey_data(pull_survey_data_from_s3()).to_csv(INPUT_PATH, index=False)
