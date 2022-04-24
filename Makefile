format:
	poetry run black bot.py
	poetry run isort bot.py

lint:
	poetry run mypy bot.py
	poetry run black --check --diff bot.py
	poetry run isort --check --diff bot.py
	poetry run pylint bot.py
