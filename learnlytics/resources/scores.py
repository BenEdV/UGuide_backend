# coding=utf-8
"""
This module contains all the endpoints for construct scores
"""
import datetime
from flask import request, jsonify, Response
from flask_restplus import Resource

from create_api import score_ns as ns
from learnlytics.extensions import db
from learnlytics.authentication import auth_required, current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.database.authorization.collection import Collection
from learnlytics.models.scores import ScoresModel


@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ScoresResource(Resource):
    """
    This class is the resource endpoint for managing models.
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets construct scores
        - __:return:__ True
        """
        data = request.get_json()
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_constructs"])

        if "start_time" in data:
            start_time = datetime.datetime.strptime(data["start_time"])
        else:
            start_time = None

        if "end_time" in data:
            end_time = datetime.datetime.strptime(data["end_time"])
        else:
            end_time = None

        if "user_ids" in data:
            user_ids = data["user_ids"]

            if user_ids == [current_identity().id]:
                authorize(collection, ["see_own_results"])
            elif user_ids != []:
                authorize(collection, ["see_anonymized_user_results"])
        else:
            user_ids = [] if "collection_ids" in data else [current_identity().id]

        if "collection_ids" in data:
            for subcollection_id in data["collection_ids"]:
                subcollection = Collection.get(subcollection_id, required=True)
                authorize(subcollection, ["see_aggregated_results"])

        scores = ScoresModel.get_construct_scores(
            collection_id=collection_id,
            user_ids=user_ids,
            collection_ids=data.get("collection_ids", []),
            construct_ids=data.get("construct_ids", []),
            activity_ids=data.get("activity_ids", None),
            start_time=start_time,
            end_time=end_time,
            out_format=data.get("format", "json")
        )

        if data.get("format", "json") == "json":
            return jsonify(scores)
        elif data["format"] == "csv":
            response = Response(
                scores,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename=scores.csv"})
            return response
