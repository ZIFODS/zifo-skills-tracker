# Zifo Skills Tracker

Zifo Skills Tracker is a full-stack web application that allows the user to visualise and query the skills of Zifo employees, as well as update their own skills. Understanding the skills that employees possess helps with resource allocation and organisation of training.

## Getting started

If you're using Windows, you will need to install a Linux environment using `WSL 2`: https://learn.microsoft.com/en-us/windows/wsl/install

Once you've configured a Linux environment, install `docker compose`: https://docs.docker.com/compose/install/

## Data

The data required to launch this application is stored in an S3 bucket, which you will need an AWS access key and AWS access secret key for. If you wish to launch it yourself or get access to the data then please see any of the following developers:

[Joseph Smith](mailto:joe.smith@zifornd.com)

[Ross Burton](mailto:ross.burton@zifornd.com)

## Getting started

There are 3 environments that can be launched using this application:

- [`prod`](./docker/docker-compose.prod.yml) - The production environment
- [`demo`](./docker/docker-compose.demo.yml) - The demo environment
- [`dev`](./docker/docker-compose.dev.yml) - The development environment

You will need to configure environment variables by adding them to the corresponding `.env` file in the root directory with the following info:

| .env.prod           | .env.demo          | .env.prod          |
| ---                 | ---                | ---                |
| SESSION_SECRET_KEY  | SESSION_SECRET_KEY | SESSION_SECRET_KEY |
| NEO4J_URI           | NEO4J_URI          | NEO4J_URI          |
| NEO4J_USER          | NEO4J_USER         | NEO4J_USER         |
| NEO4J_PASSWORD      | NEO4J_PASSWORD     | NEO4J_PASSWORD     |
| JWT_SECERET_KEY     | -                  | -                  |
| AZURE_CLIENT_ID     | -                  | -                  |
| AZURE_CLIENT_SECRET | -                  | -                  |
| AZURE_TENANT_ID     | -                  | -                  |
| AZURE_REDIRECT_URI  | -                  | -                  |

The JWT and session secret keys can be generated using `openssl rand -hex 32`. The Azure keys and Neo4j credentials should be requested from [Joe Smith](mailto:joe.smith@zifornd.com).

More information on Azure configuration can be found in the [Authentication](docs/Authentication.md) documentation.

## Running the application

Once the variables are configured, using docker compose to launch the application:

```
docker compose -f docker/docker-compose.dev.yml up -d --build
```
