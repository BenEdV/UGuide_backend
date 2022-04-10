
"""
Contains the RemindoRecipeModel, which handles all request related to recipes.
"""

import json

from learnlytics.connectors.learninglocker.models import LearningLockerSubModel
from learnlytics.connectors.learninglocker.util import make_basic_auth


class LearningLockerClientModel(LearningLockerSubModel):

    def get_client(self):
        return self.connector.get_client()

    def get_client_with_store_id(self, store_id):
        query = {
            "lrs_id": store_id
        }
        params = {
            "query": json.dumps(query)
        }
        return self.connector.get_client(params=params)

    def make_credentials_from_client(self, client_json):
        key = client_json["api"]["basic_key"]
        secret = client_json["api"]["basic_secret"]
        auth = make_basic_auth(key, secret)

        credentials = {
            "key": key,
            "secret": secret,
            "auth": auth,
            "scopes": client_json["scopes"]
        }

        return credentials

    def create_client(self, title, store_id, scopes):
        json = {
            "title": title,
            "scopes": scopes,
            "organisation": self.connector.organisation_id,
            "lrs_id": store_id
        }
        return self.connector.post_client(json=json)
