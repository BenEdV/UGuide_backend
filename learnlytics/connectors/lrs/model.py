"""
This module contains the LRS model. With this model one can connect to an xAPI compliant Learning Record Store.
"""
from bson.objectid import ObjectId
from flask import current_app
from pymongo import MongoClient
import pymongo
from urllib.parse import urlparse, parse_qs

from learnlytics.authentication.util import current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.connectors.learninglocker.util import make_basic_auth
from learnlytics.connectors.model import ConnectorModel
from learnlytics.connectors.lrs.connector import LRSConnector


class LRSModel(ConnectorModel):  # pylint: disable=too-few-public-methods
    """
    Learning Locker model uses the learning locker api to create new learning record stores
    """

    def __init__(self, db_connector):
        self.db_connector = db_connector
        settings = db_connector.settings
        xapi_base_url = settings["xapi_base_url"]
        clients = settings["clients"]
        key = clients[0]["key"]
        secret = clients[0]["secret"]
        api_version = settings["api_version"]
        print(f"Init Learning Locker model with: {xapi_base_url}, {key}, {secret}")
        self.connector = LRSConnector(xapi_base_url, key, secret, api_version)
        self.mongo = MongoClient(current_app.config["MONGO_URL"])[current_app.config["MONGO_DB"]]

        # from learnlytics.connectors.learninglocker.models.client import LearningLockerClientModel
        # from learnlytics.connectors.learninglocker.models.store import LearningLockerStoreModel
        # self.client_model = LearningLockerClientModel(self.connector)
        # self.store_model = LearningLockerStoreModel(self.connector)

    def get_info(self):
        info_dict = {}
        info_dict["keys"] = []
        settings = self.db_connector.settings
        from learnlytics.database.connector.connector import Connector
        ll_connector = Connector.get_code("learninglocker", required=True)

        if settings["xapi_base_url"] == ll_connector.settings["xapi_base_url"]:
            ll_model = ll_connector.model
            lrs = ll_model.get_store(settings["lrs_id"])
            info_dict["statement_count"] = lrs["statementCount"]
            info_dict["title"] = self.db_connector.title
            info_dict["date_added"] = lrs["createdAt"]
            info_dict["last_updated"] = lrs["updatedAt"]

        if settings["main"]:
            if authorize(self.db_connector.collection, ["see_main_lrs_write_key"], do_abort=False):
                info_dict["public_base_url"] = settings["public_base_url"]
                for client in settings["clients"]:
                    if client["scopes"] == ["statements/write", "statements/read/mine"]:
                        info_dict["keys"].append({
                            "key": client["key"],
                            "secret": client["secret"],
                            "auth": make_basic_auth(client["key"], client["secret"]),
                            "scopes": client["scopes"]
                        })
            # else:
            #     info_dict["no_access"] = "to_public_key"
        else:
            for client in settings["clients"]:
                if client["scopes"] == ["statements/write", "statements/read/mine"]:
                    if authorize(self.db_connector.collection, ["see_sec_lrs_write_key"], do_abort=False):
                        info_dict["keys"].append({
                            "key": client["key"],
                            "secret": client["secret"],
                            "auth": make_basic_auth(client["key"], client["secret"]),
                            "scopes": client["scopes"]
                        })
                elif authorize(self.db_connector.collection, ["see_sec_lrs_read_key"], do_abort=False):
                    info_dict["keys"].append({
                        "key": client["key"],
                        "secret": client["secret"],
                        "auth": make_basic_auth(client["key"], client["secret"]),
                        "scopes": client["scopes"]
                    })

        return info_dict

    def get_unprocessed_statements(self, params):
        results = []
        settings = self.db_connector.settings

        params["lrs_id"] = ObjectId(settings["lrs_id"])
        params["voided"] = False

        self.mongo.statements.ensure_index([("timestamp", pymongo.DESCENDING)])
        statements = self.mongo.statements.find(params).sort("timestamp", pymongo.DESCENDING)
        for statement in statements:
            results.append(statement["statement"])
        return results

    def get_statements(self, params):
        return self.post_process_statements(self.get_unprocessed_statements(params))

    def reset(self):
        """
        Removes all statements from the given lrs
        """
        settings = self.db_connector.settings

        params = {}
        params["lrs_id"] = ObjectId(settings["lrs_id"])

        self.mongo.statements.delete_many(params)
        return True

    # For most calls direct db access is faster
    def get_statements_through_learninglocker(self, params):
        results = []
        response = self.connector.get_statements(params=params)
        results.extend(response["statements"])

        while response["more"] != "":
            query = parse_qs(urlparse(response["more"]).query)
            cursor_id = query["cursor"][0]
            params["cursor"] = cursor_id
            response = self.connector.get_statements(params=params)
            results.extend(response["statements"])

        return results

    def post_statements(self, statements):
        return self.post_process_statements(self.connector.post_statements(json=statements))

    def post_process_statements(self, statements):
        for statement in statements:
            statement["user_id"] = self.get_user_id_of_statement(statement)

        return statements

    def get_user_id_of_statement(self, statement):
        if "actor" not in statement or "account" not in statement["actor"] or \
           "homePage" not in statement["actor"]["account"] or "name" not in statement["actor"]["account"]:
            return -1

        if statement["actor"]["account"]["homePage"] != current_identity().actor["homePage"]:
            return -1

        return int(statement["actor"]["account"]["name"])
