docker compose -f ../docker/docker-compose.dev.yml down -v;
docker compose -f ../docker/docker-compose.dev.yml up -d --build;
docker compose -f ../docker/docker-compose.dev.yml exec -it python-api poetry run python pipeline/mock_data.py;
docker compose -f ../docker/docker-compose.dev.yml exec -it python-api poetry run python pipeline/load_neo4j.py;
