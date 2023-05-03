# Zifo Skills Tracker

Zifo Skills Tracker is a full-stack web application that allows the user to visualise and query the skills of Zifo employees, as well as update their own skills.

Understanding the skills that employees possess helps with resource allocation and organisation of training.

## Getting started

If you're using Windows, you will need to install a Linux environment using `WSL 2`: https://learn.microsoft.com/en-us/windows/wsl/install

Once you've configured a Linux environment, install `docker compose`: https://docs.docker.com/compose/install/

## Getting started

There are 2 environments that can be launched using this application:

- [`prod`](./docker/docker-compose.prod.yml) - The production environment
- [`dev`](./docker/docker-compose.dev.yml) - The development environment

For production, you will need to configure environment variables by adding the following to a `.env.prod` file in the root directory:

| .env.prod           |
| ------------------- |
| SESSION_SECRET_KEY  |
| NEO4J_URI           |
| NEO4J_USER          |
| NEO4J_PASSWORD      |
| JWT_SECERET_KEY     |
| AZURE_CLIENT_ID     |
| AZURE_CLIENT_SECRET |
| AZURE_TENANT_ID     |
| AZURE_REDIRECT_URI  |
| FRONTEND_URL        |
| REACT_APP_API_URL   |

The JWT and session secret keys can be generated using `openssl rand -hex 32`.
The Azure keys and Neo4j credentials should be requested from [Joe Smith](mailto:joe.smith@zifornd.com).

More information on Azure configuration can be found in the [Authentication](docs/Authentication.md) documentation.

For the dev environment, environment variables have been hardcoded in [config.py](./app/config.py)

## Data

The data required to launch the dev environment and successfully run tests is pre-assembled in a CSV and is tracked using DVC. This CSV is used to import the data into neo4j.
To access this data, you will need to configure DVC with AWS credentials that permit access to the `zifo-ds-eu` S3 bucket. Follow the instructions [here](https://dvc.org/doc/user-guide/data-management/remote-storage/amazon-s3) to do this using the method most suitable for your setup.

Alternatively, you can generate the mock data from scratch, as shown in the following section.
**NOTE**: the mock data is generated randomly so the existing tests will fail if you regenerate the data.

Data for the prod environment is stored in a Neo4j Aura database in the cloud. To access the prod data, you will need to request the credentials from:

[Joseph Smith](mailto:joe.smith@zifornd.com)

[Ross Burton](mailto:ross.burton@zifornd.com)

It is possible to regenerate the import CSV for the prod environment from the legacy MS Forms responses using the script at [pipeline/survey_data.py].

## Running the application locally

You will need `docker compose` installed to run the application.

You can launch the dev environment in two ways:

- Using pre-assembled mock data: [run-dev.sh](./scripts/run-dev.sh)
- Generating mock data from scratch: [run-dev-fresh.sh](./scripts/test-dev.sh)

## Testing

To run the tests, simply run the [test-dev.sh](./test_docker.sh) script in the root directory.

## Running the application in production

When running in production, the Azure AD app requires that this application is running on a secure domain.
To do this, you will need to configure a reverse proxy using `nginx` and use `certbot` to generate an SSL certificate for the domain.

A [bash script](./scripts/init-letsencrypt.sh) has been acquired from a separate [repository](https://github.com/wmnnd/nginx-certbot) to automate the process of generating an SSL certificate.

Run this script once to generate the SSL certificate. The certificate should be automatically renewed after 90 days.

Once the SSL certificate has been generated, you can load the environment variables and launch the application.

You can use the [run-prod.sh] script to execute all of this.
