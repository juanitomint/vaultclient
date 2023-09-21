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
look in [main.py](https://github.com/juanitomint/vaultclient/blob/main/main.py)

.env 
this env vars are available with sabe defaults
| Variable       | default value | Description  |
|----------------|:--------------:|:------------|
| VAULT_HOSTPORT |http://localhost:8200| url for vault endpoint| 
| VAULT_PATH     |"kubernetes-access"| path in Authentication Methods
|VAULT_ROLE      |"my-api"           | Role asociated to service account in kubernetes|
|VAULT_MOUNTPOINT| secret | Fixed muuntpoint for kv stores like /services or /apis|
|VAULT_SSL_VERIFY |True| Wheather or not verify the ssl certificate, useful for self signed certs|

## Uninstall/Remove

```bash
pip uninstall tiny_vaultclient
```

## TEST


spin up a local vault instance using docker
```bash
export VAULT_ADDR='http://127.0.0.1:8200' 

make vault-up 
vault login devtoken
make vault-secret 
```


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