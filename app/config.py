from decouple import config

# MongoDB Replica Set
MONGODB_HOST = config("MONGODB_HOST", "localhost")
MONGODB_PORT = int(config("MONGODB_PORT", 27017))
MONGODB_COLLECTION = "test"
MONGODB_DATABASE = "test"

# Azure login
AZURE_CLIENT_ID = config("AZURE_CLIENT_ID", None)
AZURE_CLIENT_SECRET = config("AZURE_CLIENT_SECRET", None)
AZURE_TENANT_ID = config("AZURE_TENANT_ID", "common")
AZURE_AUTHORITY = config(
    "AZURE_AUTHORITY", f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
)
AZURE_DISCOVERY_URL = f"{AZURE_AUTHORITY}/v2.0/.well-known/openid-configuration"
AZURE_REDIRECT_URL = config("AZURE_REDIRECT_URL", None)

# Front end endpoint
FRONTEND_URL = "http://localhost:3000"

# Request session
SESSION_SECRET_KEY = config("SESSION_SECRET_KEY", None)

# JWT access token configuration
JWT_SECRET_KEY = config("JWT_SECRET_KEY", None)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
AUTH_TOKEN_EXPIRE_MINUTES = 1
