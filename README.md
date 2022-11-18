# Zifo Skills Graph

Zifo Skills Graph is a full-stack web application that allows the user to visualise and query the skills of Zifo employees. Understanding the skills that employees possess helps with resource allocation and organisation of training.

## Getting started

If you're using Windows, you will need to install a Linux environment using `WSL 2`: https://learn.microsoft.com/en-us/windows/wsl/install

Once you've configured a Linux environment, install `docker compose`: https://docs.docker.com/compose/install/

Running the following command will launch the application using production data:
```
source run-docker.sh
```

Alternatively, you can test the application using mock data:
```
source test-docker.sh
```

## Data

The data required to launch this application is stored in an S3 bucket, which you will need an AWS access key and AWS access secret key for. If you wish to launch it yourself or get access to the data then please see any of the following developers:

[Joseph Smith](mailto:joe.smith@zifornd.com)

[Ross Burton](mailto:ross.burton@zifornd.com)

[Adam Kent](mailto:adam.kent@zifornd.com)