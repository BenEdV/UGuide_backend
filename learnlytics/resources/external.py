# coding=utf-8
"""
This module contains all the endpoints for exams.
"""
from flask import request, jsonify
from flask_restplus import Resource

from create_api import external_ns as ns

from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize
from learnlytics.connectors.osiris.model import OsirisResultsModel
from learnlytics.database.connector.connector import Connector
from learnlytics.database.authorization.collection import Collection


@ns.route('/<string:external_code>/exams/minimal')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ExternalExamsMinimalResource(Resource):
    """
    The resource endpoint for a minimal list of exams from the given external resource
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, external_code):  # pylint: disable=no-self-use
        """
        Gets a list of exams from the external resource
        :return: A dictionary containing a list of recipes in minimal form
        """
        connector = Connector.get_code(external_code, required=True)

        # if authorize(connector.collection, ["see_exams"]):
        return connector.model.get_exams_minimal()


@ns.route('/<string:external_code>/<int:collection_id>/loadexam/<string:remote_exam_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ExternalLoadExamResource(Resource):
    """
    The resource endpoint for a minimal list of Remindo recipes
    """

    @auth_required
    @ns.response(201, 'Created')
    def post(self, external_code, collection_id, remote_exam_id):  # pylint: disable=no-self-use
        """
        Loads an exam from the given external resource with the id for the external
        :return: The posted recipe
        """
        connector = Connector.get_code(external_code, required=True)
        data = request.get_json()
        collection = Collection.get(collection_id, required=True)

        # if authorize(connector.collection, ["see_activities"]):
        #     if authorize(collection, ["manage_activities"]):
        return jsonify(connector.model.add_exam_to_collection(collection_id, remote_exam_id, data))


@ns.route('/<string:external_code>/loadresults')
@ns.response(204, 'No Content')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ExternalLoadResultsResource(Resource):
    """
    The resource endpoint for a minimal list of Remindo recipes
    """

    resource = {
        "osiris": OsirisResultsModel()
    }

    @auth_required
    @ns.response(200, 'Success')
    def get(self, external_code):  # pylint: disable=no-self-use
        """
        Loads an exam from the given external resource with the id for the external
        :return: The posted recipe
        """
        # external_collection = Collection.get_name(external_code, required=True)
        # course = Course.get_code(course_code, required=True)

        # if authorize(external_collection, ["see_exams"]):
        #    if authorize(course.collection, ["manage_exams"]):
        results = self.resource[external_code].get_results()
        if results == 204:
            return {}, 204
        if results == 500:
            return {}, 500

        return results


@ns.route('/<string:external_code>/recipe/<int:recipe_id>/moments')
@ns.response(204, 'No Content')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ExternalRecipeMomentsResource(Resource):
    """
    The resource endpoint for a minimal list of Remindo recipes
    """

    resource = {
        "osiris": OsirisResultsModel()
    }

    @auth_required
    @ns.response(200, 'Success')
    def get(self, external_code, recipe_id):  # pylint: disable=no-self-use
        """
        Loads an exam from the given external resource with the id for the external
        :return: The posted recipe
        """
        connector = Connector.get_code(external_code, required=True)

        results = connector.model.get_recipe_moments(recipe_id)

        return jsonify(results)


@ns.route('/<string:external_code>/moment/<int:moment_id>/candidates')
@ns.response(204, 'No Content')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ExternalMomentCandidatesResource(Resource):
    """
    The resource endpoint for a minimal list of Remindo recipes
    """

    resource = {
        "osiris": OsirisResultsModel()
    }

    @auth_required
    @ns.response(200, 'Success')
    def get(self, external_code, moment_id):  # pylint: disable=no-self-use
        """
        Loads an exam from the given external resource with the id for the external
        :return: The posted recipe
        """
        connector = Connector.get_code(external_code, required=True)

        results = connector.model.get_moment_candidates(moment_id)

        return results


@ns.route('/<string:external_code>/test')
@ns.response(204, 'No Content')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ExternalTestResource(Resource):
    """
    The resource endpoint for a minimal list of Remindo recipes
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, external_code):  # pylint: disable=no-self-use
        """
        Loads an exam from the given external resource with the id for the external
        :return: The posted recipe
        """
        # external_collection = Collection.get_name(external_code, required=True)
        # course = Course.get_code(course_code, required=True)

        # if authorize(external_collection, ["see_exams"]):
        #    if authorize(course.collection, ["manage_exams"]):

        connector = Connector.get_code(external_code, required=True)
        data = request.json

        results = connector.model.test(data)
        if results == 204:
            return {}, 204
        if results == 500:
            return {}, 500

        return results


@ns.route('/<string:external_code>/callback')
@ns.response(204, 'No Content')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ExternalCallbackResource(Resource):
    """
    The resource endpoint for callbacks made directly from an external system
    """

    @ns.response(200, 'Success')
    def post(self, external_code):  # pylint: disable=no-self-use
        """
        Sends the callback to its connector to be handled, authentication should be handled by the connector
        """
        connector = Connector.get_code(external_code, required=True)

        results = connector.model.callback(request)

        return None, 200


@ns.route('/<string:external_code>/reset')
@ns.response(204, 'No Content')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ExternalResetResource(Resource):
    """
    The resource endpoint for resetting the content of a connector
    """

    @ns.response(200, 'Success')
    def post(self, external_code):  # pylint: disable=no-self-use
        """
        Sends the reset to its connector to be handled, authentication should be handled by the connector
        """
        connector = Connector.get_code(external_code, required=True)

        results = connector.model.reset()

        return None, 200
