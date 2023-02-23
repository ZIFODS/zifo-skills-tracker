FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM base AS python-deps

RUN apt-get -y update

# Install poetry and dependencies
RUN pip install --upgrade pip
RUN pip install poetry

# Install wget for health check
RUN apt-get -y update && apt-get -y install wget

FROM python-deps as runtime

# # Create new user
RUN useradd --create-home skills-user
USER skills-user
WORKDIR /home/skills-user

COPY pyproject.toml .
RUN poetry install

# Copy source code
COPY ./app ./app
COPY .env .

# # Run the application with Docker run
CMD ["poetry", "run", "hypercorn", "app.main:app", "--reload", "--bind", "0.0.0.0:8080"]
