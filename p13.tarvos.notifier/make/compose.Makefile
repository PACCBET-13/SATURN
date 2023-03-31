.PHONY: compose-build
compose-build: ## Build or rebuild services
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) build

.PHONY: compose-up
compose-up: ## Create and start containers
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) up -d

.PHONY: broker-compose-up
broker-compose-up: ## Create and start containers
	docker compose -f docker/rabbitmq-compose.yml --env-file $(ENV_FILE) up -d

.PHONY: compose-logs
compose-logs: ## View output from containers
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) logs

.PHONY: compose-ps
compose-ps: ## List containers
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) ps

.PHONY: compose-ls
compose-ls: ## List running compose projects
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) ls

.PHONY: compose-start
compose-start: ## Start services
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) start

.PHONY: compose-restart
compose-restart: ## Restart services
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) restart

.PHONY: compose-stop
compose-stop: ## Stop services
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) stop

.PHONY: compose-down
compose-down: ## Stop and remove containers, networks
	docker compose -f docker/docker-compose.yml --env-file $(ENV_FILE) down --remove-orphans
