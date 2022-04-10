# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project period (3 4)
# (C) Copyright Utrecht University (Department of Information and Computing Sciences)
"""
This module contains all the endpoints for periods.
"""

from flask import request
from flask_restplus import Resource

from create_api import periods_ns as ns
from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize
from learnlytics.database.authorization.collection import Collection
from learnlytics.models.course_instances import CourseInstances as CourseInstancesModel
from learnlytics.models.periods import Periods as PeriodsModel
import learnlytics.database.studydata as md


@ns.route('/')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class PeriodsResource(Resource):
    """
    This class is the resource endpoint for all periods.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Gets a list of all available periods.
        - __:return:__ a list of json objects of all the available periods.

        """
        authorize(Collection.get_root_collection(required=True), ["see_periods"])

        result_dic = PeriodsModel.get_periods()
        return result_dic

    @auth_required
    @ns.response(201, 'Created')
    def post(self):  # pylint: disable=no-self-use
        """
        Adds a new period.
        - __return__: True if successful
        """
        # read json request data
        data = request.json

        authorize(Collection.get_root_collection(required=True), ["manage_periods"])

        PeriodsModel.add_period(
            data["name"],
            data["start_date"],
            data["end_date"]
        )

        return {"success": "true"}, 201


@ns.route('/<int:period_id>')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
@ns.doc(params={"period_id": "The id of the period"})
class PeriodResource(Resource):
    """
    This class is the resource endpoint for a single period.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, period_id):  # pylint: disable=no-self-use
        """
        Gets a period instance with the given period_id.
        - __:param *period_id*__: id of the period instance to get.
        - __:return__: a json object of the requested period instance.
        """
        authorize(Collection.get_root_collection(required=True), ["see_periods"])

        return PeriodsModel.get_period(period_id)

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, period_id):  # pylint: disable=no-self-use
        """
        Deletes a period with the given period_id.
        - __:param *period_id*__: The id of the period to delete.
        - __:return__: True
        """
        period = md.Period.get(period_id, required=True)

        authorize(Collection.get_root_collection(required=True), ["manage_periods"])

        PeriodsModel.delete_period(period)

        return None, 204


@ns.route('/<int:period_id>/instances')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
@ns.doc(params={"period_id": "The id of the period"})
class PeriodInstancesResource(Resource):
    """
    This class is the resource endpoint for a single period.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, period_id):  # pylint: disable=no-self-use
        """
        Gets a period instance with the given period_id.
        - __:param *period_id*__: id of the period instance to get.
        - __:return__: a json object of the requested period instance.
        """
        # authorize(Collection.get_root_collection(required=True), ["see_periods"])

        return CourseInstancesModel.get_course_instances_for_period(period_id)
