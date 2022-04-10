# coding=utf-8
"""
This module contains all the endpoints for constructs
"""
from flask_restplus import Resource

from create_api import type_ns as ns
from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.role import Role
from learnlytics.database.construct.construct import ConstructModel
from learnlytics.database.studydata.activity import Activity
from learnlytics.models.connectors import ConnectorsModel


@ns.route('/models')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ModelTypesResource(Resource):
    """
    This class is the resource endpoint for managing models.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all models.
        - __:return:__ True
        """
        return ConstructModel.get_all_types()


@ns.route('/activities')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityTypesResource(Resource):
    """
    This class is the resource endpoint for managing activity types
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all activity types.
        - __:return:__ True
        """
        return Activity.get_activity_types()


@ns.route('/material')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class MaterialTypesResource(Resource):
    """
    This class is the resource endpoint for managing study material types
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all study material types.
        - __:return:__ True
        """
        return Activity.get_material_types()


@ns.route('/survey')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class MaterialTypesResource(Resource):
    """
    This class is the resource endpoint for managing study material types
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Get information about the survey type
        - __:return:__ True
        """
        return Activity.get_survey_type()


@ns.route('/visibility')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class VisibilityTypesResource(Resource):
    """
    This class is the resource endpoint for managing activity visibility options
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all activity types.
        - __:return:__ True
        """
        return Activity.get_visibility_types()


@ns.route('/remotes')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class RemotesResource(Resource):
    """
    This class is the resource endpoint for retrieving remotes/connectors that we support
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all remote types.
        - __:return:__ True
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_connectors"])

        return ConnectorsModel.get_collection_connectors(collection)


@ns.route('/construct_relations')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConstructRelationsResource(Resource):
    """
    This class is the resource endpoint for retrieving construct relations that we support
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all construct relation types.
        - __:return:__ True
        """
        return ConstructModel.get_construct_relation_types()


@ns.route('/activity_relations')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityRelationsResource(Resource):
    """
    This class is the resource endpoint for retrieving construct relations that we support
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all activity relation types.
        - __:return:__ True
        """
        return Activity.get_activity_relation_types()


@ns.route('/construct_activity_relations')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConstructActivityRelationsResource(Resource):
    """
    This class is the resource endpoint for retrieving construct -> activity relations that we support
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all construct activity relation types.
        - __:return:__ True
        """
        return ConstructModel.get_construct_activity_relation_types()


@ns.route('/user_roles')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class UserRoleTypeResource(Resource):
    """
    This class is the resource endpoint for retrieving user roles that we support
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all construct activity relation types.
        - __:return:__ True
        """
        return Role.get_all_names()
