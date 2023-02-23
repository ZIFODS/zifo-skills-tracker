# Zifo Skills Tracker

Zifo Skills Tracker is a full-stack application that allows users to create, read, update, and delete skills of Zifo employees. It is currently still in active development.

## Getting started

You will need to configure environment variables by adding them to a `.env` file in the root directory with the following info:

- JWT_SECERET_KEY
- SESSION_SECRET_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID
- AZURE_REDIRECT_URI

The JWT and session secret keys can be generated using `openssl rand -hex 32`. The AWS keys must be granted access to the S3 bucket that stores the schema. The Azure keys should be requested from [Joe Smith](mailto:joe.smith@zifornd.com).

More information on Azure configuration can be found in the [Authentication](docs/Authentication.md) documentation.

## Running the application

Once the variables are configured, using docker to launch the application:

```
docker-compose up -d --build
```
