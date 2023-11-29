import json
import logging

import boto3

logger = logging.Logger("logger")


def get_secret(secret_name: str, aws_region: str):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=aws_region)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    return json.loads(get_secret_value_response["SecretString"])
