build:
	docker compose up -d --build
	docker compose exec web poetry run python app/db.py

up:
	docker compose up -d
	docker compose exec web poetry run python app/db.py

test:
	docker compose exec web poetry run python -m pytest "tests" -p no:warnings

coverage:
	docker compose exec web poetry run python -m pytest "tests" -p no:warnings --cov="."

lint:
	docker compose exec web poetry run flake8 .

lint_black: lint
	docker compose exec web poetry run black . --check
	docker compose exec web poetry run /bin/sh -c "isort **/*.py --check-only"

black:
	docker compose exec web poetry run black .
	docker compose exec web poetry run /bin/sh -c "isort **/*.py"

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

down:
	docker compose down
