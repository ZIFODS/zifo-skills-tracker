docker compose -f docker/docker-compose.prod.yml down;
bash scripts/init-letsencrypt.sh;
docker compose -f docker/docker-compose.prod.yml up -d --build;
