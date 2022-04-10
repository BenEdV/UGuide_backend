# coding=utf-8
"""
This module contains all the endpoints for connectors.
"""
from flask import request
from flask_restplus import Resource, marshal, fields

from create_api import connector_ns as ns
from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize
import learnlytics.database.studydata as md
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.connector.connector import Connector

from learnlytics.models.connectors import ConnectorsModel


@ns.route('/')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConnectorsResource(Resource):
    """
    This class is the resource endpoint for all connectors.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets a list of all activites linked to given collection
        - __:param *collection_id*:__ The id of the collection for which we want the connectors
        - __:return:__ A list of JSON objects of all the linked connectors.
        """

        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_connectors"])

        return ConnectorsModel.get_collection_connectors(collection)

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use
        """
        Get the connector with the given connector id.
        - __:param *collection_id*:__ The id of the collection the connector belongs to.
        - __:param *connector_id*:__ The id of the connector to get.
        - __:return:__ A JSON object of the requested connector.
        """
        data = request.json
        collection = Collection.get(collection_id, required=True)

        return ConnectorsModel.new_connector(collection.id, data)


@ns.route('/<int:connector_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConnectorResource(Resource):
    """
    This is a specific connector resource endpoint.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, connector_id):  # pylint: disable=no-self-use
        """
        Get the connector with the given connector id.
        - __:param *collection_id*:__ The id of the collection the connector belongs to.
        - __:param *connector_id*:__ The id of the connector to get.
        - __:return:__ A JSON object of the requested connector.
        """
        connector = Connector.get(connector_id, required=True)

        authorize(connector.collection, ["see_connectors"])

        return ConnectorsModel.get_connector(connector_id)

    @auth_required
    def put(self, collection_id, connector_id):
        """
        Function changing the visibility of a test.
        - __:param *collection_id*:__ The collection_id the connector is in.
        - __:param *connector_id*:__ The connector id specifying which connector should be changed.
        - __:param *visible*:__ The new visibility value.
        """
        data = request.json
        connector = Connector.get(connector_id, required=True)

        authorize(connector.collection, ["manage_connectors"])

        return ConnectorsModel.update_connector(connector_id, data)

    @auth_required
    def delete(self, collection_id, connector_id):
        """
        Deletes the given connector
        :param collection_id: id of the collection to which the connector is connected
        :param connector_id: id of the connector
        :return: 204
        """
        connector = Connector.get(connector_id, required=True)

        authorize(connector.collection, ["manage_connectors"])

        ConnectorsModel.delete_connector(connector.id)

        return None, 204
