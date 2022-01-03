include $(PWD)/.env
SHELL := /usr/bin/bash
.DEFAULT_GOAL := help

# AutoDoc
# -------------------------------------------------------------------------
.PHONY: help
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help

# Docker
# -------------------------------------------------------------------------

# API
# -------------------------------------------------------------------------
.PHONY: build-docker-api
build-docker-api: ## Build the API Dockerfile. Optional variables BUILDKIT, DOCKER_API_IMAGE and DOCKER_API_TAG
	cd app && \
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_API_IMAGE=$(or $(DOCKER_API_IMAGE),core-api) \
		DOCKER_API_TAG=$(or $(DOCKER_API_TAG),test) && \
	docker build -t $$DOCKER_API_IMAGE:$$DOCKER_API_TAG .
.DEFAULT_GOAL := build-docker-api

.PHONY: lint-docker-api
lint-docker-api: ## Lint the API Dockerfile
	cd app && docker run --rm -i -v ${PWD}:/hadolint -v ${PWD}/.hadolint.yml:/hadolint/.hadolint.yml --workdir=/hadolint hadolint/hadolint < Dockerfile
.DEFAULT_GOAL := lint-docker-api

# MongoDB
# -------------------------------------------------------------------------
.PHONY: build-docker-db
build-docker-db: ## Build the DB Dockerfile. Optional variables BUILDKIT, DOCKER_DB_IMAGE, DOCKER_DB_TAG
	cd database && \
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_DB_IMAGE=$(or $(DOCKER_DB_IMAGE),core-db) \
		DOCKER_DB_TAG=$(or $(DOCKER_DB_TAG),test) && \
	docker build -t $$DOCKER_DB_IMAGE:$$DOCKER_DB_TAG .
.DEFAULT_GOAL := build-docker-db


# Docker-compose
# -------------------------------------------------------------------------
.PHONY: run-app-attached
run-app-attached: ## Run docker-compose with the terminal attached. Supply BUILDKIT=1/0, DOCKER_API_IMAGE=core-api and DOCKER_API_TAG=test
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_API_IMAGE=$(or $(DOCKER_API_IMAGE),core-api) \
		DOCKER_API_TAG=$(or $(DOCKER_API_TAG),test) \
		DOCKER_DB_IMAGE=$(or $(DOCKER_DB_IMAGE),core-db) \
		DOCKER_DB_TAG=$(or $(DOCKER_DB_TAG),test) && \
	docker-compose up --build --remove-orphans db && docker-compose rm -fsv
.DEFAULT_GOAL := run-app-attached





