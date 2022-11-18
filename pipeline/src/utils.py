'''
Global variables representing values in the input and output CSVs.
'''

import boto3
import botocore
from pathlib import Path
import sys
import os
import pandas as pd
from enum import Enum

ROOT_DIR = (Path(__file__).parent / "../../").resolve()
sys.path.append(str(ROOT_DIR))


class MissingEnvVarError(Exception):
    pass


class AuthError(Exception):
    pass


class EnviroVars(Enum):
    """

    """
    try:
        AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    except KeyError:
        raise MissingEnvVarError("Missing AWS access key and secret in environment variables")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "zifo-ds-eu").strip("/")
    AWS_BUCKET_DIR = os.getenv("AWS_BUCKET_DIR", "skill-graph/skills_survey_input").strip("/")
    LOCAL_INPUT_DIR = os.getenv("LOCAL_INPUT_DIR", "pipeline/input").strip("/")
    LOCAL_IMPORT_DIR = os.getenv("LOCAL_IMPORT_DIR", "pipeline/import").strip("/")
    SURVEY_NAME_FIELD = os.getenv("SURVEY_NAME_FIELD", "Name")
    SURVEY_DATETIME_FIELD = os.getenv("SURVEY_DATETIME_FIELD", "Completion time")
    SURVEY_EMAIL_FIELD = os.getenv("SURVEY_EMAIL_FIELD", "Email")


def pull_survey_data_from_s3() -> pd.DataFrame:
    """
    Load any CSV files from the skills survey folder into memory as a Pandas DataFrame. Where multiple CSV files
    are found, data are merged into a single DataFrame. Data could contain multiple entries and therefore should
    be filtered accordingly.

    NOTE: Boto3 will search for the following environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_BUCKET_NAME
    - AWS_BUCKET_DIR

    Returns
    -------
    Pandas.DataFrame

    Raises
    ------
    AuthError
        Invalid credentials for AWS, check env variables are correct.
    ValueError
        Could not resolve S3 bucket. Check that the target directory on AWS or the AWS bucket name are correct.
    ClientError
        Some other error with AWS client
    """
    try:
        s3 = boto3.client('s3')  # again assumes boto.cfg setup, assume AWS S3
        bucket_contents = s3.list_objects_v2(
            Bucket=EnviroVars.AWS_BUCKET_NAME.value,
            Prefix=EnviroVars.AWS_BUCKET_DIR.value
        )["Contents"]
        xls_in_bucket = [key["Key"] for key in bucket_contents if Path(key["Key"]).suffix in [".xls", ".xlsx"]]
        data = pd.concat(
            [
                pd.read_excel(f"s3://{EnviroVars.AWS_BUCKET_NAME.value}/{xls}")
                for xls in xls_in_bucket
            ]
        ).reset_index(drop=True)
        data[EnviroVars.SURVEY_DATETIME_FIELD.value] = pd.to_datetime(data[EnviroVars.SURVEY_DATETIME_FIELD.value])
        return data
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            raise ValueError(
                "Could not resolve S3 bucket. Check that the target directory on AWS or the AWS bucket name are correct."
            )
        if e.response['Error']['Code'] == "401":
            raise AuthError("Invalid credentials for AWS, check env variables are correct.")
        else:
            raise


def filter_survey_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Given Skills Survey data as a Pandas DataFrame, groups the data by unique identifiers and
    then keeps the most recent record from each individual.

    Parameters
    ----------
    data: Pandas.DataFrame

    Returns
    -------
    Pandas.DataFrame
    """
    most_recent_data = [
        df.sort_values(EnviroVars.SURVEY_DATETIME_FIELD.value, ascending=True).iloc[-1] for _, df in
        data.groupby([EnviroVars.SURVEY_NAME_FIELD.value, EnviroVars.SURVEY_EMAIL_FIELD.value])
    ]
    return pd.DataFrame(most_recent_data)


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

