## @ start
.PHONY: run
run: ## run application in localhost
	@pipenv run python manage.py runserver

## @ format
.PHONY: format
format: ## perform formatting on all files with isort and blue
	@pipenv run isort --gitignore .
	@pipenv run black .

## @ test
.PHONY: test test_coverage test_coverage_view
test: ## perform tests
	@pipenv run pytest -s

test_coverage: ## run tests and generate coverage html
	@pipenv run pytest -s --cov-report html --cov=apps

test_coverage_view: ## run http server in localhost:9000 with coverage results
	@pipenv run python -m http.server 9000 --directory htmlcov

## @ requirements
.PHONY: requirements
requirements: ## generate requirements.txt and requirements.dev.txt
	@pipenv run pipenv requirements > requirements.txt
	@pipenv run pipenv requirements --dev > requirements.dev.txt

## @ Help
.PHONY: help
help: ## show help commands
	@pipenv run python help.py