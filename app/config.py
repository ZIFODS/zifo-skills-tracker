import os

from decouple import config

from app.utils.security.secrets import get_secret


class Env:
    DEV = "dev"
    PRODUCTION = "production"


PROD_ENV = False
if os.environ.get("SKILLS_ENV") == Env.PRODUCTION:
    PROD_ENV = True

# Front end endpoint
FRONTEND_URL = config("FRONTEND_URL", "http://localhost:3000")

# AWS
AWS_REGION = config("AWS_REGION", "eu-west-2")
AWS_SECRET_KMS_KEY = config("AWS_SECRET_KMS_KEY", "")
AWS_SECRET_NAME_NEO4J = config("AWS_SECRET_NAME_NEO4J", "")
AWS_SECRET_NAME_AZURE = config("AWS_SECRET_NAME_AZURE", "")
AWS_SECRET_NAME_API = config("AWS_SECRET_NAME_API", "")

# MongoDB
MONGODB_HOST = config("MONGODB_HOST", "localhost")
MONGODB_PORT = config("MONGODB_PORT", 27017, cast=int)
MONGODB_COLLECTION = "test"
MONGODB_DATABASE = "test"

# Request session
if PROD_ENV:
    SESSION_SECRET = get_secret(AWS_SECRET_NAME_API, AWS_REGION, AWS_SECRET_KMS_KEY)
    SESSION_SECRET_KEY = SESSION_SECRET["session_secret"]
else:
    SESSION_SECRET_KEY = config("SESSION_SECRET_KEY", None)

# JWT access token configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
AUTH_TOKEN_EXPIRE_MINUTES = 1
if PROD_ENV:
    JWT_SECRET_KEY = get_secret(AWS_SECRET_NAME_API, AWS_REGION, AWS_SECRET_KMS_KEY)
    JWT_SECRET_KEY = SESSION_SECRET["jwt_secret"]
else:
    JWT_SECRET_KEY = config("JWT_SECRET_KEY", None)

# neo4j
if PROD_ENV:
    NEO4J_SECRET = get_secret(AWS_SECRET_NAME_NEO4J, AWS_REGION, AWS_SECRET_KMS_KEY)
    NEO4J_URI = NEO4J_SECRET["uri"]
    NEO4J_USERNAME = NEO4J_SECRET["username"]
    NEO4J_PASSWORD = NEO4J_SECRET["password"]
else:
    NEO4J_URI = config("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = config("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = config("NEO4J_PASSWORD", "test")

# Azure AD
if PROD_ENV:
    AZURE_SECRET = get_secret(AWS_SECRET_NAME_AZURE, AWS_REGION, AWS_SECRET_KMS_KEY)
    AZURE_CLIENT_ID = AZURE_SECRET["client_id"]
    AZURE_TENANT_ID = AZURE_SECRET["tenant_id"]
    AZURE_CLIENT_SECRET = AZURE_SECRET["client_secret"]
    AZURE_REDIRECT_URI = AZURE_SECRET["redirect_uri"]
else:
    AZURE_CLIENT_ID = config("AZURE_CLIENT_ID", None)
    AZURE_CLIENT_SECRET = config("AZURE_CLIENT_SECRET", None)
    AZURE_TENANT_ID = config("AZURE_TENANT_ID", "common")
    AZURE_REDIRECT_URI = config("AZURE_REDIRECT_URI", None)
AZURE_AUTHORITY = config(
    "AZURE_AUTHORITY", f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
)
AZURE_DISCOVERY_URL = f"{AZURE_AUTHORITY}/v2.0/.well-known/openid-configuration"

# PRIMA
PRIMA_AUTH_URL = config("PRIMA_AUTH_URL", "")
PRIMA_DATA_URL = config("PRIMA_DATA_URL", "")

PRIMA_AUTH_PAYLOAD = {
    "client_id": config("PRIMA_CLIENT_ID", ""),
    "client_secret_id": config("PRIMA_CLIENT_SECRET_ID", ""),
    "token_unique_id": config("PRIMA_TOKEN_UNIQUE_ID", "")
}