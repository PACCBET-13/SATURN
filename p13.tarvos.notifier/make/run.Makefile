APP_HOST_CURRENT=$(if $(APP_HOST),$(APP_HOST),0.0.0.0)
APP_PORT_CURRENT=$(if $(APP_PORT_INTERNAL),$(APP_PORT_INTERNAL),8000)
APP_WORKERS_CURRENT=$(if $(APP_WORKERS),$(APP_WORKERS),1)
APP_LOG_LEVEL_CURRENT=$(if $(APP_LOG_LEVEL),$(APP_LOG_LEVEL),info)

.PHONY: run
run: ## Run application
	poetry run gunicorn \
	    --bind $(APP_HOST_CURRENT):$(APP_PORT_CURRENT) \
		--worker-class uvicorn.workers.UvicornWorker \
		--workers $(APP_WORKERS_CURRENT) \
		--log-level $(APP_LOG_LEVEL_CURRENT) \
		--chdir cmd/app \
		main:app
