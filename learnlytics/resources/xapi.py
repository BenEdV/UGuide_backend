# coding=utf-8
"""
This module contains functions for xapi
"""

from create_api import xapi_ns as ns
from flask_restplus import Resource
from flask import request
import requests
import base64
from sqlalchemy import func

from learnlytics.extensions import db
from learnlytics.connectors.xapi_moodle.load_content import new_statement
from learnlytics.database.connector.connector import Connector


@ns.route('/<path:request_path>')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class xapiResource(Resource):
    """
    This class for the hello world test.
    """

    @ns.response(200, 'Success')
    def get(self, request_path):  # pylint: disable=no-self-use
        """
        This redirects the xapi request to the learninglocker connection
        """

        response = requests.get(
            url=f"http://learninglocker_xapi:8081/data/xAPI/{request_path}",
            headers=request.headers,
            json=request.json,
            params=request.args
        )

        return response.json()

    @ns.response(200, 'Success')
    def post(self, request_path):  # pylint: disable=no-self-use
        """
        This redirects the xapi request to the learninglocker connection
        """

        response = requests.post(
            url=f"http://learninglocker_xapi:8081/data/xAPI/{request_path}",
            headers=request.headers,
            json=request.json,
            params=request.args
        )

        if response.status_code == requests.codes.ok:
            # Determine which collection the lrs belongs to
            auth_encoded = request.headers["Authorization"].split(" ")[1]
            auth_bytes = auth_encoded.encode("ascii")
            auth_decoded_bytes = base64.b64decode(auth_bytes)
            auth = auth_decoded_bytes.decode("ascii")
            collection_tuple = db.session.query(Connector.collection_id).filter(
                Connector.implementation == 'lrs',
                Connector.settings["clients"].astext.like(f"%{auth.split(':')[0]}%")
            ).one_or_none()
            if collection_tuple:
                collection_id, = collection_tuple
                new_statement(request.json, collection_id)

        return response.json()

    @ns.response(200, 'Success')
    def put(self, request_path):  # pylint: disable=no-self-use
        """
        This redirects the xapi request to the learninglocker connection
        """

        response = requests.put(
            url=f"http://learninglocker_xapi:8081/data/xAPI/{request_path}",
            headers=request.headers,
            json=request.json,
            params=request.args
        )

        return response.json()
