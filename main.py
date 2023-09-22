import json
import os

import tinyvaultclient
from config import Config

vclient = tinyvaultclient.Client(Config)

# set VAULT_ADDR for local
os.environ["VAULT_ADDR"] = "http://localhost:8200"
# disable ssl for local
Config.VAULT_SSL_VERIFY = False

defaultPath = ""
# Create a VaultClient
# List secrets
secrets = vclient.listSecrets(defaultPath)
# Print secrets
print("List secrets", json.dumps(secrets, indent=4, sort_keys=True))

# read versioned secret
secret = vclient.readSecret(defaultPath, "testapp")
print("Read one secret", json.dumps(secret, indent=4, sort_keys=True))


scret = vclient.writeSecret(
    defaultPath,
    "my_new_secret",
    {
        "test": "secret",
        "from": __file__,
        "package": __package__,
        "name": __name__,
    },
)
# deleted version
secret = vclient.readSecret(defaultPath, "my_new_secret")
print("Read deleted version secret", json.dumps(secret, indent=4, sort_keys=True))


secret = vclient.deleteSecret(defaultPath, "my_new_secret")
# destroyed version
secret = vclient.readSecret(defaultPath, "my_new_secret")
print("Read destroyed version secret", json.dumps(secret, indent=4, sort_keys=True))
