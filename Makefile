BACKEND_SERVICE=web
PROJECT_NAME={{cookiecutter.app_name}}

# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 20

# Common

all: run

## Runs application. Builds, creates, starts, and attaches to containers for a service. | Common
run:
	@docker-compose up $(BACKEND_SERVICE)

## Rebuild web container
build:
	@docker-compose build

## Runs application on service ports.
debug:
	@docker-compose run --service-ports --rm $(BACKEND_SERVICE)

## Runs application with `docker-compose up`.
up:
	@docker-compose up

## Stops application. Stops running container without removing them.
stop:
	@docker-compose stop

## Removes stopped service containers.
clean:
	@docker-compose down

## Runs command `bash` commands in docker container.
bash:
	@docker-compose exec $(BACKEND_SERVICE) bash

## Run Flask debug shell.
shell:
	@docker-compose exec $(BACKEND_SERVICE) flask shell
# Help

## Shows help.
help:
	@echo ''
	@echo 'Usage:'
	@echo ''
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
		    if (index(lastLine, "|") != 0) { \
				stage = substr(lastLine, index(lastLine, "|") + 1); \
				printf "\n ${GRAY}%s: \n\n", stage;  \
			} \
			helpCommand = substr($$1, 1, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			if (index(lastLine, "|") != 0) { \
				helpMessage = substr(helpMessage, 0, index(helpMessage, "|")-1); \
			} \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''

# Docs

# Linters & tests

## Formats code with `pylint`.
lint:
	@docker-compose run --rm $(BACKEND_SERVICE) pylint $(PROJECT_NAME) tests

# Database

## Runs PostgreSQL UI. | Database
psql:
	@docker-compose exec postgres psql -U postgres

## Upgrades database.
upgrade:
	@docker-compose run --rm $(BACKEND_SERVICE) flask db upgrade

## Makes migration.
migrate:
	@docker-compose run --rm $(BACKEND_SERVICE) flask db migrate

## Runs tests.
test:
	@docker-compose run --rm $(BACKEND_SERVICE) pytest
