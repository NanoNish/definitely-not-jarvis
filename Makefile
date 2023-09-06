run:
	@cd content && npm run develop &
	@cd server && poetry run python3 main.py &

setup-unix:
	curl -sSL https://install.python-poetry.org | python3 -
	cd content && npm install && cd ..
	cd server && poetry install && cd ..

setup-win:
	curl -sSL https://install.python-poetry.org | py -
	cd content && npm install && cd ..
	cd server && poetry install & &cd ..