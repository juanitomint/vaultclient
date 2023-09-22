import logging
import os

import hvac
from hvac.api.auth_methods import Kubernetes

# from config import Config


class Client:
    def __init__(self, config={}, logger=None):
        """
        The VaultClient class represents a client for interacting with a Vault service. It has the following attributes:
        url: A string representing the URL of the Vault service.
        role: A string representing the role for authentication with the Vault service.
        mount_point: A string representing the mount point for accessing secrets in the Vault service.
        logger: A logger object for logging messages related to the Vault client.
        client: An instance of the Vault client used to interact with the Vault service.
        """
        self.url = config.VAULT_HOSTPORT
        self.role = config.VAULT_ROLE
        self.login_mount_point = config.VAULT_PATH
        self.mount_point = config.VAULT_MOUNTPOINT
        self.verify = getattr(config, "VAULT_SSL_VERIFY" , True
        if logger is None:
            self.setup_logger()
        self.client = hvac.Client()
        self.client = self.getClient()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(name)s %(funcName)s: %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        self.logger = logger

    def getClient(self):
        """
        Get the client object.

        Returns:
            The client object if it is authenticated, otherwise a new client object.
        """
        if self.client and self.client.is_authenticated():
            self.logger.info("Client still good to go!")
            return self.client
        else:
            self.logger.info("Client not authenticated")
            return self.newClient()

    def newClient(self):
        """
        Creates a new client for accessing the Vault API.

        Returns:
            hvac.Client: The client object for accessing the Vault API.

        Raises:
            Exception: If an error occurs during the creation of the client.
        """
        try:
            client = hvac.Client(url=self.url, verify=self.verify)
            if os.path.isfile("/var/run/secrets/kubernetes.io/serviceaccount/token"):
                self.vault_login()
            else:
                self.logger.info(
                    "/var/run/secrets/kubernetes.io/serviceaccount/token.... not found"
                )
            if not client.is_authenticated():
                raise
            return client
        except Exception as err:
            self.logger.error(str(err))
            raise

    def vault_login(self):
        """
        Logs into the vault using the provided token and retrieves a JWT for authentication.

        Parameters:
        - None

        Returns:
        - None
        """

        token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        f = open(token_path)
        jwt = f.read()
        response = Kubernetes(self.client.adapter).login(
            role=self.role, jwt=jwt, mount_point=self.login_mountpoint
        )
        self.logger.debug(response)

    def writeSecret(self, path, secretName, secret):
        """
        Write a secret to the key-value store.

        Args:
            path (str): The path to store the secret.
            secretName (str): The name of the secret.
            secret (str): The secret to be stored.

        Returns:
            None
        """
        updict = {
            "00_IF_YOU_ARE_A_HUMAN_READ_ME_CAREFULLY └[ ∵ ]┘": """Any changes in this specific
         path will be lost at random intervals. You must add your changes in a different Vault path""",
            "maintainer": "O11Y-API",
        }
        vaultsecret = {**updict, **secret}
        self.client.secrets.kv.v2.create_or_update_secret(
            mount_point=self.mount_point,
            path=f"{path}/{secretName}",
            secret=vaultsecret,
        )

    def deleteSecret(self, path, secretName):
        """
        Deletes a secret from the Vault.

        Parameters:
            path (str): The path where the secret is stored.
            secretName (str): The name of the secret to be deleted.

        Returns:
            None
        """
        self.client.secrets.kv.v2.delete_metadata_and_all_versions(
            mount_point=self.mount_point, path=f"{path}/{secretName}"
        )

    def listSecrets(self, path):
        try:
            secrets = self.client.secrets.kv.v2.list_secrets(
                mount_point=self.mount_point, path=path
            )
            return secrets["data"]["keys"]
        except Exception as err:
            self.logger.critical(str(err))

    def readSecret(self, path, secretName):
        metadata = self.read_secret_metadata(path, secretName)
        if metadata is None:
            self.logger.error(f"Secret {secretName} not found")
            return
        if self.is_secret_latest_version_deleted(metadata):
            self.logger.error(f"Secret {secretName} has been deleted")
            return
        if self.is_latest_version_destroyed(metadata):
            self.logger.error(f"Secret {secretName} has been destroyed")
            return

        current_version = metadata["data"]["current_version"]
        secret = self.client.secrets.kv.v2.read_secret_version(
            mount_point=self.mount_point,
            path=f"{path}/{secretName}",
            version=current_version,
        )
        return secret["data"]

    def read_secret_metadata(self, path, secretName):
        """
        Reads the metadata of a secret.

        Args:
            path (str): The path of the secret.
            secretName (str): The name of the secret.

        Returns:
            dict: The metadata of the secret.
        """
        try:
            secret_metadata = self.client.secrets.kv.v2.read_secret_metadata(
                mount_point=self.mount_point, path=f"{path}/{secretName}"
            )
            return secret_metadata
        except Exception as err:
            self.logger.critical(str(err))

    def is_secret_latest_version_deleted(self, metadata):
        current_version = metadata["data"]["current_version"]
        if current_version is None:
            return True

        # check if it has deletion_time
        return metadata["data"]["versions"][str(current_version)]["deletion_time"] != ""

    def is_latest_version_destroyed(self, metadata):
        """
        Determines if the latest version of a secret has been deleted.

        Args:
            secret_metadata (dict): The metadata for the secret.

        Returns:
            bool: True if the latest version of the secret has been deleted, False otherwise.
        """
        # Get the latest version
        current_version = metadata["data"]["current_version"]
        if current_version is None:
            return True

        # Check if the latest version is destroyed
        return metadata["data"]["versions"][str(current_version)]["destroyed"]
