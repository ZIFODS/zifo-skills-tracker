bash run-dev.sh;
docker compose -f ../docker/docker-compose.dev.yml exec -it python-api poetry run python -m pytest -v --cov=app --cov-report=xml --cov-report=term-missing;
