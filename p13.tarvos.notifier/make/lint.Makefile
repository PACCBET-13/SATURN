.PHONY: lint
lint: ## Run linters
	make lint-isort
	make lint-flake
	make lint-mypy


.PHONY: lint-isort
lint-isort: ## Run isort linter
	poetry run isort .

.PHONY: lint-flake8
lint-flake:  ## Run flake8 linter
	poetry run flake8

.PHONY: lint-mypy
lint-mypy: ## Run mypy linter
	poetry run mypy .
