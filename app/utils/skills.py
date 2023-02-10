import os
from enum import Enum

import pandas as pd


class MissingEnvVarError(Exception):
    pass


class AuthError(Exception):
    pass


class EnviroVars(Enum):
    """ """

    try:
        AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    except KeyError:
        raise MissingEnvVarError(
            "Missing AWS access key and secret in environment variables"
        )
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "zifo-ds-eu").strip("/")
    AWS_BUCKET_DIR = os.getenv("AWS_BUCKET_DIR", "skill-graph").strip("/")
    SCHEMA_FILENAME = os.getenv("SCHEMA_FILENAME", "skills-schema.xlsx").strip("/")
    LOCAL_INPUT_DIR = os.getenv("LOCAL_INPUT_DIR", "data").strip("/")


def pull_skills_schema_from_s3() -> pd.DataFrame:
    """
    Pulls the skills schema Excel file from AWS S3 bucket and loads it into a pandas DataFrame.

    NOTE: Boto3 will search for the following environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_BUCKET_NAME
    - AWS_BUCKET_DIR

    Returns
    -------
    Pandas.DataFrame
    """

    try:
        return pd.read_excel(
            f"s3://{EnviroVars.AWS_BUCKET_NAME.value}/{EnviroVars.AWS_BUCKET_DIR.value}/ \
            {EnviroVars.SCHEMA_FILENAME.value}"
        )

    except PermissionError:
        raise PermissionError(
            "The AWS credentials supplied as environment variables are invalid for this bucket."
        )

    except FileNotFoundError:
        raise FileNotFoundError(
            f"The file {EnviroVars.SCHEMA_FILENAME.value} does not exist in the \
            {EnviroVars.AWS_BUCKET_DIR.value} directory of the {EnviroVars.AWS_BUCKET_NAME.value} \
            bucket."
        )
