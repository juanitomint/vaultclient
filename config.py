import os

import toml
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    """
    Check if the given value is equivalent to a boolean True.

    :param value: The value to be checked.
    :type value: Any

    :return: True if the value is equivalent to boolean True, False otherwise.
    :rtype: bool
    """
    if value:
        return value.lower() in ["true", "yes", "on", "1"]
    return False


class Config:
    PYPROJECT = toml.load("pyproject.toml")["tool"]["poetry"]
    VAULT_HOSTPORT = os.environ.get("VAULT_HOSTPORT", "http://localhost:8200")

    VAULT_PATH = os.environ.get("VAULT_PATH", "kubernetes-infra-prod-us-east-1")
    VAULT_ROLE = os.environ.get("VAULT_ROLE", "observability-api")
    VAULT_MOUNTPOINT = os.environ.get("VAULT_MOUNTPOINT", "secret")
    VAULT_SSL_VERIFY = os.environ.get("VAULT_SSL_VERIFY", True)
