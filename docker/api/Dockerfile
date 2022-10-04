FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --dev

FROM base AS runtime

# Install wget for health check
RUN apt-get -y update && apt-get -y install wget

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home skills_user
WORKDIR /home/skills_user
USER skills_user

# Install application into container
COPY ./app ./app
COPY ./pipeline ./pipeline

# Run the application with Docker run
CMD ["hypercorn", "app.main:app", "--reload", "--bind", "0.0.0.0:8080"]