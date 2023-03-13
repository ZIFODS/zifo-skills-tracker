from decouple import config

# MongoDB Replica Set
MONGODB_HOST = config("MONGODB_HOST", "localhost")
MONGODB_PORT = config("MONGODB_PORT", 27017, cast=int)
MONGODB_COLLECTION = "test"
MONGODB_DATABASE = "test"

# neo4j
NEO4J_URI = config("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = config("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = config("NEO4J_PASSWORD", "test")

# Azure login
AZURE_CLIENT_ID = config("AZURE_CLIENT_ID", None)
AZURE_CLIENT_SECRET = config("AZURE_CLIENT_SECRET", None)
AZURE_TENANT_ID = config("AZURE_TENANT_ID", "common")
AZURE_AUTHORITY = config(
    "AZURE_AUTHORITY", f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
)
AZURE_DISCOVERY_URL = f"{AZURE_AUTHORITY}/v2.0/.well-known/openid-configuration"
AZURE_REDIRECT_URI = config("AZURE_REDIRECT_URI", None)

# Front end endpoint
FRONTEND_URL = "http://localhost:3000"

# Request session
SESSION_SECRET_KEY = config("SESSION_SECRET_KEY", None)

# JWT access token configuration
JWT_SECRET_KEY = config("JWT_SECRET_KEY", None)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
AUTH_TOKEN_EXPIRE_MINUTES = 1
