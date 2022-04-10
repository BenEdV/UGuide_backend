"""
This module contains the resources for displaying information on the homepage
"""

from flask import request, jsonify
from flask_restplus import Resource

from create_api import home_ns as ns
from learnlytics.authentication.authentication_manager import auth_required
from learnlytics.authentication.util import current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.models.activities import ActivitiesModel


@ns.route('/activities/')
@ns.response(401, 'Unauthorized')
class HomeActivitiesResource(Resource):
    """
    Allows a user to retrieve all activities they can participate in
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Returns all activities they can participate in
        """
        user = current_identity()

        return jsonify(ActivitiesModel.get_all_activities(user.id))


@ns.route('/surveys/')
@ns.response(401, 'Unauthorized')
class HomeSurveysResource(Resource):
    """
    Allows a user to retrieve all activities they can participate in
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Returns all activities they can participate in
        """
        user = current_identity()

        return jsonify(ActivitiesModel.get_all_activities(user.id, type_name="survey"))
