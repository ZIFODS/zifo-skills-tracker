# Zifo Skills Tracker

Zifo Skills Tracker is a full-stack web application that allows the user to visualise, query and update the skills of Zifo employees.

Understanding the skills that employees possess helps with resource allocation and organisation of training.

The production instance can be found at [https://skills.zifo-tech.com](https://skills.zifo-tech.com). You will need a Zifo Microsoft account to access it.

## Contents

- [Quickstart](#quickstart)
- [Environments](#environments)
- [Installation](#installation)
- [Data](#data)
- [Running the application locally](#running-the-application-locally)
- [Testing](#testing)
- [Running the application in production](#running-the-application-in-production)

## Quickstart

If you're using Windows, you will need to install a Linux environment using `WSL 2`: https://learn.microsoft.com/en-us/windows/wsl/install

Once you've configured a Linux environment, install `docker compose`: https://docs.docker.com/compose/install/

To launch the dev environment with randomly generated mock data, run the following script:

```bash
./scripts/run-dev-fresh.sh
```

## Environments

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

## Installation

To install the Python backend as a developer, you will need to install `poetry` and then use the following commands:

```bash
poetry install
poetry shell
```

Installation of the frontend requires `npm` and the following commands to be run:

```bash
cd frontend
npm install
```

## Data

The data required to launch the dev environment and successfully run tests is pre-assembled in a CSV and is tracked using DVC. This CSV is used to import the data into neo4j.
To access this data, you will need to configure DVC with AWS credentials that permit access to the `zifo-ds-eu` S3 bucket. Follow the instructions [here](https://dvc.org/doc/user-guide/data-management/remote-storage/amazon-s3) to do this using the method most suitable for your setup.

One way to do this is as follows:

```bash
dvc remote modify s3 --local access_key_id <access_key_id>
dvc remote modify s3 --local secret_access_key <secret_access_key>
dvc pull --recursive
```

Alternatively, you can generate the mock data from scratch, as shown in the following section.

**NOTE**: the mock data is generated randomly so the existing tests will fail if you regenerate the data.

**NOTE**: if you generate the mock data from scratch, this will overwrite the DVC tracked file if you have it downloaded so it will need to be pulled again.

Data for the prod environment is stored in a Neo4j Aura database in the cloud. To access the prod data, you will need to request the credentials from:

[Joseph Smith](mailto:joe.smith@zifornd.com)

[Ross Burton](mailto:ross.burton@zifornd.com)

It is possible to regenerate the import CSV for the prod environment from the legacy MS Forms responses using the script at [pipeline/survey_data.py].

## Running the application locally

You will need `docker compose` installed to run the application.

You can launch the dev environment in two ways:

- Using pre-assembled mock data: [run-dev.sh](./scripts/run-dev.sh)
- Generating mock data from scratch: [run-dev-fresh.sh](./scripts/test-dev.sh)

Run the script as follows:

```bash
./scripts/run-dev.sh
```

## Testing

To run the tests, simply run the [test-dev.sh](./test_docker.sh) script in the root directory.

## Running the application in production

When running in production, the Azure AD app requires that this application is running on a secure domain.
To do this, you will need to configure a reverse proxy using `nginx` and use `certbot` to generate an SSL certificate for the domain.

A [bash script](./scripts/init-letsencrypt.sh) has been acquired from a separate [repository](https://github.com/wmnnd/nginx-certbot) to automate the process of generating an SSL certificate.

Run this script once to generate the SSL certificate. The certificate should be automatically renewed after 90 days.

Once the SSL certificate has been generated, you can load the environment variables and launch the application.

You can use the [run-prod.sh](./scripts/run-prod.sh) script to execute all of this.
