run:
	@cd server && poetry run python3 main.py &
	@cd content && npm run develop &

setup-unix:
	curl -sSL https://install.python-poetry.org | python3 -
	cd server && poetry install && cd ..

setup-win:
	curl -sSL https://install.python-poetry.org | py -
	poetry install