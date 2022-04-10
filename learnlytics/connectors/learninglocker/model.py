
"""
This module contains the Learning Locker model
"""
import logging

from learnlytics.connectors.model import ConnectorModel
from learnlytics.connectors.learninglocker.connector import LearningLockerConnector

logger = logging.getLogger("learninglocker")


class LearningLockerModel(ConnectorModel):  # pylint: disable=too-few-public-methods
    """
    Learning Locker model uses the learning locker api to create new learning record stores
    """

    def __init__(self, db_connector):
        self.db_connector = db_connector
        settings = db_connector.settings
        api_base_url = settings["api_base_url"]
        username = settings["username"]
        password = settings["password"]
        logger.debug(f"Init Learning Locker model with: {api_base_url}, {username}, {password}")
        self.connector = LearningLockerConnector(api_base_url, username, password)

        from learnlytics.connectors.learninglocker.models.client import LearningLockerClientModel
        from learnlytics.connectors.learninglocker.models.store import LearningLockerStoreModel
        self.client_model = LearningLockerClientModel(self.connector)
        self.store_model = LearningLockerStoreModel(self.connector)

    def create_new_store(self, title):
        store = self.store_model.create_store(title)
        client = self.client_model.get_client_with_store_id(store["_id"])[0]
        credentials = self.client_model.make_credentials_from_client(client)
        return (store, credentials)

    def create_new_client(self, title, store_id, scopes):
        client = self.client_model.create_client(title, store_id, scopes)
        credentials = self.client_model.make_credentials_from_client(client)

        return credentials

    def get_store(self, store_id):
        store = self.store_model.get_store(store_id)
        return store

    def get_info(self):
        info = {
            "title": "Learning Locker",
            "api_base_url": self.db_connector.settings["api_base_url"],
            "xapi_base_ur": self.db_connector.settings["xapi_base_url"]
        }

        return info
