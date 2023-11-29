import json
import logging

import boto3


def get_secret(secret_name: str, aws_region: str, aws_kms_key: str):
    # Create a Secrets Manager client
    logging.info(secret_name)
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=aws_region)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    return json.loads(get_secret_value_response[aws_kms_key])
