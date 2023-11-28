FROM python:3.10-slim as base
LABEL maintainer="Joseph Smith"
LABEL version="0.1.0"
LABEL description="FastAPI server for Zifo Skills Tracker"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install wget for health check
RUN apt-get -y update && apt-get -y install wget

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml .

RUN poetry install

# Copy source code
COPY ./app ./app
RUN mkdir ./data

CMD ["poetry", "run", "hypercorn", "app.main:app", "--reload", "--bind", "0.0.0.0:8080"]
