# coding=utf-8
"""
This module contains all the endpoints for the user settings
"""
from flask import request
from flask_restplus import Resource

from create_api import currentuserns as ns
from learnlytics.authentication import auth_required
from learnlytics.authentication.util import current_identity
from learnlytics.models.user_settings import CourseUserSettings as UserSettingsModel
from learnlytics.resources.restplus_models.expect_models import post_user_settings_fields


@ns.route('/settings')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class UserSettingsResource(Resource):
    """
    This class is the resource endpoint for managing user settings.
    """

    @auth_required
    @ns.response(200, 'Success')
    @ns.expect(post_user_settings_fields)
    def post(self):  # pylint: disable=no-self-use
        """
        Saves the preferences for the current user.
        - __:body__: The body contains the user, course_id and preferences
        - __:return:__ True
        """
        data = request.get_json()
        user = current_identity()
        return UserSettingsModel.upsert_user_settings(user, data)

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Gets the preferences for the current user.
        - __:return:__ The JSON containig the preferences of the current user
        """
        user = current_identity()
        return UserSettingsModel.get_user_settings(user.id)


@ns.route('/persons')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class UserSettingsResource(Resource):
    """
    This class is the resource endpoint for managing user settings.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Gets the preferences for the current user.
        - __:return:__ The JSON containig the preferences of the current user
        """
        user = current_identity()
        return UserSettingsModel.get_user_persons(user.id)
