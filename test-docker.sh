TEST_ENV=true; \
docker compose down -v; \
docker compose up -d --build; \
docker compose exec -T python-api python pipeline/src/run_pipeline.py; \
docker compose exec -T python-api pytest -vv ./integration_test;