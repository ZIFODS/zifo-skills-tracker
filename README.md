# Zifo Skills Update

Zifo Skills Update is a full-stack application that allows users to create, read, update, and delete skills of Zifo employees. It is currently still in active development.

## Getting started

For the backend, you will need to download [Python 3.10](https://www.python.org/downloads/) and then install and activate a virtual environment by entering the following commands sequentially from the root directory:

```bash
pip install poetry
poetry install
poetry shell
```

Once the environment has been activated, run `bash run-api.sh` to launch the API server.

For the frontend, you will need to install [Node.js](https://nodejs.org/en/download/) and then install the dependencies by entering the following commands sequentially from the root directory:

```bash
cd frontend
npm install
```

Once the packages are installed, run `npm start` to launch the frontend server.
