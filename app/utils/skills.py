import pandas as pd
from decouple import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = config("AWS_BUCKET_NAME", "zifo-ds-eu").strip("/")
AWS_BUCKET_DIR = config("AWS_BUCKET_DIR", "skill-graph").strip("/")
SCHEMA_FILENAME = config("SCHEMA_FILENAME", "skills-schema.xlsx").strip("/")
LOCAL_INPUT_DIR = config("LOCAL_INPUT_DIR", "data").strip("/")


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
            f"s3://{AWS_BUCKET_NAME}/{AWS_BUCKET_DIR}/{SCHEMA_FILENAME}"
        )

    except PermissionError:
        raise PermissionError(
            "The AWS credentials supplied as environment variables are invalid for this bucket."
        )

    except FileNotFoundError:
        raise FileNotFoundError(
            f"The file {SCHEMA_FILENAME} does not exist in the {AWS_BUCKET_DIR} directory of \
            the {AWS_BUCKET_NAME} bucket."
        )
