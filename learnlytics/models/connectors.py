"""
This module contains the model for connectors
"""

from flask_restplus import abort

from learnlytics.authentication import current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.extensions import db
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.connector.connector import Connector
import learnlytics.database.studydata as md


class ConnectorsModel(object):  # pylint: disable=no-init
    """
    Contains a methods which get available connectors
    """

    @staticmethod
    def get_connector(connector_id):
        """
        Get the connector of the given collection with the given connector id
        :param connector_id: The id of the connector to get
        :return: 404 or a dictionary containing the connector data
        """
        # ids = [connector_id]
        # connector = md.Connector.get(connector_id, required=True)
        # for tail_connector in connector.tail_connectors:
        #     ids.append(tail_connector.id)
        # return ConnectorsModel.get_connectors(ids)[0]
        return ConnectorsModel.get_connectors([connector_id])[0]

    @staticmethod
    def get_collection_connectors(collection):
        """
        """
        connector_ids = []
        for connector in collection.connectors:
            connector_ids.append(connector.id)
        return ConnectorsModel.get_connectors(connector_ids)

    @staticmethod
    def get_connectors(connector_ids):
        """
        Returns a list of connectors for the ids provided
        """
        res = []

        # !!!!!!!
        # Database calls
        # !!!!!!!

        # connectors
        connectors = Connector.query.filter(Connector.id.in_(connector_ids)).all()
        if connectors == []:
            return []
        collection = connectors[0].collection

        for connector in connectors:
            if connector.collection != collection:
                abort(409, "Request contains connectors from different collections")

        # !!!!!!!
        # Creating dictionary
        # !!!!!!!
        for connector in connectors:
            connector_dict = connector.get_info()

            res.append(connector_dict)

        res.sort(key=lambda q: q["id"])

        return res

    @staticmethod
    def new_connector(collection_id, connector_data):
        collection = Collection.get(collection_id, required=True)

        if connector_data["implementation"] == "lrs" and authorize(collection, ["manage_sec_lrs"]):
            connector = collection.create_lrs_for_collection(title=connector_data["title"], main=False)

        if connector_data["implementation"] == "remindo" and authorize(collection, ["manage_connectors"]):
            if "code" in connector_data:
                code = connector_data["code"]
            else:
                code = connector_data["title"].lower().replace(" ", "_")
            connector = Connector(
                collection_id=collection_id,
                title=connector_data["title"],
                code=code,
                implementation="remindo",
                settings={
                    "base_url": connector_data["remindo"]["base_url"],
                    "uuid": connector_data["remindo"]["uuid"],
                    "secret": connector_data["remindo"]["secret"],
                }
            )

        db.session.add(connector)
        db.session.commit()

        return [ConnectorsModel.get_connector(connector.id)]

    @staticmethod
    def update_connector(connector_id, connector_data):
        connector = Connector.get(connector_id)

        if "title" in connector_data:
            connector.title = connector_data["title"]
        if "settings" in connector_data:
            connector.settings = connector_data["settings"]

        db.session.commit()

        return ConnectorsModel.get_connector(connector.id)

    @staticmethod
    def delete_connector(connector_id):
        connector = Connector.get(connector_id, required=True)

        db.session.delete(connector)
        db.session.commit()
