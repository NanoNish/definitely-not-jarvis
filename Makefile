run:
	@cd server && poetry run python3 main.py &
	@cd content && npm run develop &
