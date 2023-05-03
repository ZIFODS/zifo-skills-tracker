docker compose -f ../docker/docker-compose.prod.yml down -v;
docker compose -f ../docker/docker-compose.prod.yml up -d --build;
