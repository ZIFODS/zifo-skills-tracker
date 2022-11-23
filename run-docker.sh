export TEST_ENV=false; \
docker compose down -v; \
docker compose up -d --build; \
docker compose exec -T python-api python pipeline/src/run_pipeline.py;
