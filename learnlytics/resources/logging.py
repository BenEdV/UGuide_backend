# coding=utf-8
"""
This module contains all the endpoints for reqlogging user activities.
"""
from flask import request, Response
from flask_restplus import Resource, marshal, abort, fields
from flask_jwt_extended import get_jwt_identity, get_jwt_claims, get_jti, get_raw_jwt
from datetime import datetime
import json
from sqlalchemy import and_

from create_api import loggingns as ns
from learnlytics.authentication import auth_required
from learnlytics.authentication.util import current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.role import Role
from learnlytics.database.authorization.user import User, UserRole
from learnlytics.database.learnlyticslogging.requestlog import RequestLog
from learnlytics.models.user_logging import LoggingState as LoggingStateModel
from learnlytics.resources.restplus_models.expect_models import post_logging_state_fields, post_logging_event_fields, \
    post_report_fields


@ns.route('/state')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class StateLogging(Resource):
    """
    This class is the resource endpoint for reqlogging angular state changes.
    """

    @auth_required
    @ns.response(200, 'Success')
    @ns.expect(post_logging_state_fields)
    def post(self):  # pylint: disable=no-self-use
        """
        Saves information about the state change for the current user.
        - __:body__: The body contains the user_id, from_state, to_state, timestamp.
        - __:return:__ True
        """
        data = request.get_json()
        user = current_identity()
        session_id = get_raw_jwt()["jti"]

        LoggingStateModel.add_state(user, session_id, data)
        return True, 201


@ns.route('/event')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class EventLogging(Resource):
    """
    This class is the resource endpoint for reqlogging angular event occurrences, such as button presses.
    """

    @auth_required
    @ns.response(200, 'Success')
    @ns.expect(post_logging_event_fields)
    def post(self):  # pylint: disable=no-self-use
        """
        Saves information about the event occurrences for the current user.
        - __:body__: The body contains the user_id, current_state, details, timestamp.
        - __:return:__ True
        """
        data = request.get_json()
        user = current_identity()
        # time = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        # current_state = json.dumps(data["current_state"])
        # LoggingStateModel.add_details_change(user, data["current_state"], data["details"], data["timestamp"])
        return True


@ns.route('/report')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class SumReport(Resource):
    """
    This class is the resource endpoint for retrieving a report on the number of log ins
    """

    @auth_required
    @ns.response(200, 'Success')
    @ns.expect(post_report_fields)
    def post(self):  # pylint: disable=no-self-use
        """
        Saves information about the event occurrences for the current user.
        - __:body__: The body contains the user_id, current_state, details, timestamp.
        - __:return:__ True
        """

        root = Collection.get_root_collection(required=True)
        authorize(root, ["see_usage_report"])

        data = request.get_json()

        start_time = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S")

        requests = RequestLog.query.filter(and_(
            RequestLog.request_path == data["path"],
            RequestLog.date_added.between(start_time, end_time))).all()

        users_dict = {}
        for log_request in requests:
            if log_request.user_id in users_dict:
                users_dict[log_request.user_id] += 1
            else:
                users_dict[log_request.user_id] = 1

        return users_dict


@ns.route('/request_logs')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class RequestReport(Resource):
    """
    This class is the resource endpoint for retrieving a report on the number of log ins
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Saves information about the event occurrences for the current user.
        - __:body__: The body contains the user_id, current_state, details, timestamp.
        - __:return:__ True
        """
        root = Collection.get_root_collection(required=True)
        if authorize(root, ["see_usage_report"], do_abort=False):
            student_role = Role.get_name("student", required=True)
            students = User.query.join(UserRole).filter(UserRole.role_id == student_role.id).all()
            user_ids = [student.id for student in students]
        else:
            user_ids = [current_identity().id]

        logs = LoggingStateModel.request_log_report(user_ids)
        response = Response(
            logs,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=logs.csv"})
        return response


@ns.route('/state_logs')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class EventRequest(Resource):
    """
    This class is the resource endpoint for retrieving a report on the number of log ins
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Saves information about the event occurrences for the current user.
        - __:body__: The body contains the user_id, current_state, details, timestamp.
        - __:return:__ True
        """
        root = Collection.get_root_collection(required=True)
        if authorize(root, ["see_usage_report"], do_abort=False):
            student_role = Role.get_name("student", required=True)
            students = User.query.join(UserRole).filter(UserRole.role_id == student_role.id).all()
            user_ids = [student.id for student in students]
        else:
            user_ids = [current_identity().id]

        logs = LoggingStateModel.state_log_report(user_ids)
        response = Response(
            logs,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=logs.csv"})
        return response


@ns.route('/thermos_logs')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ThermosRequest(Resource):
    """
    This class is the resource endpoint for retrieving a report on the number of log ins
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Saves information about the event occurrences for the current user.
        - __:body__: The body contains the user_id, current_state, details, timestamp.
        - __:return:__ True
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["see_usage_report"])

        data = request.get_json()

        if "start_time" in data:
            start_time = datetime.strptime(data["start_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            start_time = datetime.fromtimestamp(0)

        if "end_time" in data:
            end_time = datetime.strptime(data["end_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            end_time = datetime.utcnow()

        logs = LoggingStateModel.thermos_log_report(start_time, end_time)
        response = Response(
            logs,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=logs.csv"})
        return response


@ns.route('/thermos_survey_logs')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ThermosSurveyRequest(Resource):
    """
    This class is the resource endpoint for retrieving a report on the number of log ins
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Saves information about the event occurrences for the current user.
        - __:body__: The body contains the user_id, current_state, details, timestamp.
        - __:return:__ True
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["see_usage_report"])

        data = request.get_json()

        if "start_time" in data:
            start_time = datetime.strptime(data["start_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            start_time = datetime.fromtimestamp(0)

        if "end_time" in data:
            end_time = datetime.strptime(data["end_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            end_time = datetime.utcnow()

        logs = LoggingStateModel.thermos_survey_report(start_time, end_time)
        response = Response(
            logs,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=logs.csv"})
        return response
