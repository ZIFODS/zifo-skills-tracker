# Zifo Skills Graph

Zifo Skills Graph is currently in development but is expected to be a full-stack web application that allows the user to visualise and query the skills of Zifo employees. Understanding the skills that employees possess will aid the company with resource allocation and training organisation.

## Getting started

To run this application, all you need installed is `docker compose`. Follow the instructions here to get started: https://docs.docker.com/compose/install/

For now, the data required by neo4j is a csv with a single skill on each line for each consultant. You can generate this from the original skills xlsx file using [pipeline.py](./pipeline/old/etc/pipeline.py). The generated csv should be stored in the [import](./pipeline/src/import/) folder prior to launch.

Once data is present, run the following command in a terminal from the root directory to launch the application:

```
bash run-docker.sh
```