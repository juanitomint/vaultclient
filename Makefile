IMAGE_REPOSITORY  ?= juanitomint/vaultclient
CURRENT_DIR = $(shell pwd)
GIT_LAST_TAG=$(shell git tag --sort=committerdate|tail -n 1)
GIT_COMMIT=$(shell git rev-parse --short HEAD)
GIT_TAG         ?=$(or ${CI_COMMIT_TAG},$(or ${GIT_LAST_TAG}, ${GIT_COMMIT} ) )
IMAGE_TAG         ?= ${GIT_TAG}
VAULT_ADDR=http://localhost:8200
help:
	@grep -E '^[\/a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'	
.PHONY: build
build: ## Build python package
	poetry build
.PHONY: publish
publish: ## Publish package to pypi
	poetry publish

.PHONY: docker-build
docker-build: ## Build docker image using latest as cache
	echo "building: ${IMAGE_REPOSITORY}:${IMAGE_TAG}"
	# docker pull ${IMAGE_REPOSITORY}:latest || true
	DOCKER_BUILDKIT=1 docker build --cache-from ${IMAGE_REPOSITORY}:latest -t ${IMAGE_REPOSITORY}:latest . --build-arg IMAGE_TAG=${IMAGE_TAG}
	docker tag ${IMAGE_REPOSITORY}:latest ${IMAGE_REPOSITORY}:${IMAGE_TAG}
	docker images ${IMAGE_REPOSITORY}:latest
  
.PHONY: docker-push 
docker-push: ## Push docker image to remote ${IMAGE_REPOSITORY}
	docker push ${IMAGE_REPOSITORY}:${IMAGE_TAG}
	docker push ${IMAGE_REPOSITORY}:latest

.PHONY: docker-test
docker-test: ## test file using docker image and .env variables
	docker run -it --rm -v \${CURRENT_DIR}:/workspace --env-file .env -p 5000:5000	${IMAGE_REPOSITORY}:latest

.PHONY: docker-test-bash
docker-test-bash: ## test the docker image but gives yuou a shell
	docker run -it --rm -v \${CURRENT_DIR}:/workspace --env-file .env	${IMAGE_REPOSITORY}:latest bash

.PHONY: deps
deps:  ## config virtual env and install dependencies using poetry
	pip install poetry
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.create true
	poetry install
.PHONY: local
local: ## installs pre-commit hook (WIP)
	poetry run pre-commit install

.PHONY: lint 
lint: ## Show code lints using black flake8 and isort
	poetry run flake8 ./
	poetry run black ./ --check
	poetry run isort ./ --check

.PHONY: fix
fix: ## Fix code lints using black flake8 and isort
	poetry run black ./ 
	poetry run flake8 ./
	poetry run isort ./ 




.PHONY: cover
cover: ## runs tests
	poetry run coverage run -m unittest discover

.PHONY: cover/report
cover/report: ## Shows coverage Report
	poetry run coverage report

.PHONY: cover/xml
cover/xml: ## Creates coverage Report
	poetry run coverage xml

.PHONY: vault-up
vault-up: ## Spin up a vault development server use it with  export VAULT_ADDR='http://127.0.0.1:8200'
	@docker run \
	--rm --detach --name vault -p 8200:8200 \
	-e 'VAULT_DEV_ROOT_TOKEN_ID=devtoken' \
	-e 'VAULT_ADDR=https://localhost:8200' \
	-e 'VAULT_SKIP_VERIFY=true' \
	--cap-add=IPC_LOCK hashicorp/vault ;\
	sleep 3
	vault login devtoken
	
.PHONY: vault-secret	
vault-secret: ## Create a new version of secrets
	vault kv put /secret/testapp dbname=pato password=most_secure_secret last_updated="$$(date)"
	vault kv get /secret/testapp

.PHONY: vault-down 
vault-down: ## Removes docker vault container
	docker rm -fv vault

.PHONY: clean ## Cleans up local environment
clean:
	docker rm -fv vault
	docker-compose down
	rm -rf ./.venv
	rm -rf ./.pytest_cache
	rm -rf ./__pycache__
	rm -rf tests/__pycache__
	rm -rf api/__pycache__


.PHONY: printvars
printvars: ## Prints make variables
	$(foreach V, $(sort $(.VARIABLES)), \
	$(if $(filter-out environment% default automatic, $(origin $V)),$(warning $V=$($V) ($(value $V)))) \
	)
