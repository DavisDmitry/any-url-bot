format:
	poetry run black any_url_bot
	poetry run isort any_url_bot

lint:
	poetry run mypy any_url_bot
	poetry run black --check --diff any_url_bot
	poetry run isort --check --diff any_url_bot
	poetry run pylint any_url_bot

docker-up:
	sudo docker compose up -d --remove-orphans --build
