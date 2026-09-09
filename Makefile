.PHONY: api web test lint stack
api:
	cd services/api && uvicorn app.main:app --reload --port 8000
web:
	pnpm --filter @prajna/web dev
test:
	cd services/api && pytest -q
lint:
	cd services/api && ruff check app tests
stack:
	docker compose up --build
