docker compose down -v; \
docker compose up -d --build; \
docker compose exec -T python-api python ./pipeline/src/neo4j_load.py;