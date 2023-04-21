# Zifo Skills Tracker

Zifo Skills Tracker is a full-stack web application that allows the user to visualise and query the skills of Zifo employees, as well as update their own skills. 

Understanding the skills that employees possess helps with resource allocation and organisation of training.

## Getting started

If you're using Windows, you will need to install a Linux environment using `WSL 2`: https://learn.microsoft.com/en-us/windows/wsl/install

Once you've configured a Linux environment, install `docker compose`: https://docs.docker.com/compose/install/

## Getting started

There are 3 environments that can be launched using this application:

- [`prod`](./docker/docker-compose.prod.yml) - The production environment
- [`demo`](./docker/docker-compose.demo.yml) - The demo environment
- [`dev`](./docker/docker-compose.dev.yml) - The development environment

You will need to configure specific environment variables depending on the environment you want to launch.

You can simply add them to the corresponding `.env` file in the root directory with the following info:

| .env.prod           | .env.demo          | .env.dev           |
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
| FRONTEND_URL        | -                  | -                  |
| REACT_APP_API_URL   | -                  | -                  |

The JWT and session secret keys can be generated using `openssl rand -hex 32`. The Azure keys and Neo4j credentials should be requested from [Joe Smith](mailto:joe.smith@zifornd.com).

More information on Azure configuration can be found in the [Authentication](docs/Authentication.md) documentation.

## Data

The data required to launch the dev and demo environments is stored in an S3 bucket. Data for the prod environment is stored in a Neo4j Aura database in the cloud. To access the data, you will need to request the credentials from

[Joseph Smith](mailto:joe.smith@zifornd.com)

[Ross Burton](mailto:ross.burton@zifornd.com)


## Running the application locally

Once the environment variables are configured, load them using the following command:

```
source .env.dev
```

Use docker compose to launch the application:

```
docker compose -f docker/docker-compose.dev.yml up -d --build
```

## Running the application in production

When running in production, the Azure AD app requires that this application is running on a secure domain. To do this, you will need to configure a reverse proxy using `nginx` and use `certbot` to generate an SSL certificate for the domain.

A [bash script](./init-letsencrypt.sh) has been acquired from a separate [repository](https://github.com/wmnnd/nginx-certbot) to automate the process of generating an SSL certificate.

Run this script once to generate the SSL certificate. The certificate should be automatically renewed after 90 days.

Once the SSL certificate has been generated, you can load the environment variables and launch the application using the following command:

```
source .env.prod &&
docker compose -f docker/docker-compose.prod.yml up -d --build
```