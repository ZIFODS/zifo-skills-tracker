docker compose -f docker/docker-compose.dev.yml down -v;
docker compose -f docker/docker-compose.dev.yml up -d --build;
docker compose -f docker/docker-compose.dev.yml exec -it python-api poetry run python tests/utils/load_mock_data.py;
docker compose -f docker/docker-compose.dev.yml exec -it python-api poetry run python -m pytest -v --cov=app --cov-report=xml --cov-report=term-missing;
