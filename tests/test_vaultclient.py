import os
import unittest

# from unittest.mock import MagicMock
import tinyvaultclient
from config import Config


class NewClinetTest(unittest.TestCase):
    def setUp(self):
        # set VAULT_ADDR for local
        os.environ["VAULT_ADDR"] = "http://localhost:8200"

        self.client = tinyvaultclient.Client(Config)

    def test_new_client_success(self):
        # Test creating a new client successfully

        self.assertEqual(self.client.client.is_authenticated(), True)
