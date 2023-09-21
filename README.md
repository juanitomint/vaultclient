# Python Vault client

A simple client for read, list, write and delete secrets from  Vault

## INSTALLATION

```bash
pip install tiny_vaultclient
```

or with poetry
```bash
poetry add tiny_vaultclient
```
## USAGE
look in [main.py](./main.py)

.env 
this env vars are available with sabe defaults

VAULT_HOSTPORT = os.environ.get("VAULT_HOSTPORT", "http://localhost:8200")

VAULT_PATH = os.environ.get("VAULT_PATH", "kubernetes-access")
VAULT_ROLE = os.environ.get("VAULT_ROLE", "my-api")
VAULT_MOUNTPOINT = os.environ.get("VAULT_MOUNTPOINT", "secret")
VAULT_SSL_VERIFY = os.environ.get("VAULT_SSL_VERIFY", True)


## Uninstall/Remove

```bash
pip uninstall tiny_vaultclient
```

## TEST


spin up a local vault instance using docker
```bash
export VAULT_ADDR='http://127.0.0.1:8200' 
make install 
make vault-up 
vault login devtoken
make vault-secret 
make test-docker 
```
Dcocker compose will spin up a database, adminer and podinfo

you can use podman to check environment variables passed to container

 ![http://localhost:9898/env](https://github.com/juanitomint/vault-env-helper/blob/main/img/podinfo.png?raw=true)

or  access the db using adminer

 ![http://localhost:8080](https://github.com/juanitomint/vault-env-helper/blob/main/img/adminer.png?raw=true)

## HELP
```bash
cover/report         Shows coverage Report
cover                runs tests
cover/xml            Creates coverage Report
deps                 config virtual env and install dependencies using poetry
docker-build         Build docker image using latest as cache
docker-push          Push docker image to remote ${IMAGE_REPOSITORY}
docker-test-bash     test the docker image but gives yuou a shell
docker-test          test file using docker image and .env variables
fix                  Fix code lints using black flake8 and isort
lint                 Show code lints using black flake8 and isort
local                installs pre-commit hook (WIP)
printvars            Prints make variables
vault-down           Removes docker vault container
vault-secret         Create a new version of secrets
vault-up             Spin up a vault development server use it with  export VAULT_ADDR='http://127.0.0.1:8200'
```