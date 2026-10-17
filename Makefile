up:
	docker compose up -d --build

down:
	docker compose down

clean:
	docker compose down -v

test:
	pytest -v

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .