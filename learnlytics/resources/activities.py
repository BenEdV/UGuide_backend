# coding=utf-8
"""
This module contains all the endpoints for activities.
"""
import json
from flask import request, send_from_directory, current_app, jsonify, abort, send_file, Response
from flask_restplus import Resource

from create_api import activity_ns as ns
from learnlytics.analyse.exam import calculate_inter_item_correlation, calculate_rir_value, average_grade, \
    average_duration
from learnlytics.analyse.question import update_question_properties
from learnlytics.authentication import auth_required
from learnlytics.authentication.util import current_identity
from learnlytics.authorization.manager import authorize
import learnlytics.database.studydata as md
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.role import Role
from learnlytics.database.authorization.user import User, UserRole

from learnlytics.models.activities import ActivitiesModel


@ns.route('/')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivitiesResource(Resource):
    """
    This class is the resource endpoint for all activities.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets a list of all activites linked to given collection
        - __:param *collection_id*:__ The id of the collection for which we want the activities
        - __:return:__ A list of JSON objects of all the linked activities.
        """

        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_activities"])

        return jsonify(ActivitiesModel.get_collection_activities(collection))

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use
        """
        Get the activity with the given activity id.
        - __:param *collection_id*:__ The id of the collection the activity belongs to.
        - __:param *activity_id*:__ The id of the activity to get.
        - __:return:__ A JSON object of the requested activity.
        """
        if request.headers["Content-Type"] == "application/json":
            # Activity has no attachments
            data = request.json
            collection = Collection.get(collection_id, required=True)

            if not isinstance(data, list):
                data = [data]

            activities = []

            authorize(collection, ["manage_activities"])

            for activity in data:
                activities.append(ActivitiesModel.new_activity(collection.id, activity))

            return jsonify(activities)
        if request.headers["Content-Type"].startswith("multipart/form-data"):
            data = json.loads(request.form.get("metadata"))
            collection = Collection.get(collection_id, required=True)

            if isinstance(data, list):
                abort(401, "Activities with attachments must be uploaded individually")

            authorize(collection, ["manage_activities"])

            files = request.files.getlist("files")
            activity = ActivitiesModel.new_activity(collection.id, data, files)

            return jsonify([activity])

        abort(401, f"Unsupported Content-Type: {request.headers['Content-Type']}")


@ns.route('/<string:type_name>')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivitiesTypeResource(Resource):
    """
    This class is the resource endpoint for all activities.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, type_name):  # pylint: disable=no-self-use
        """
        Gets a list of all activites linked to given collection
        - __:param *collection_id*:__ The id of the collection for which we want the activities
        - __:return:__ A list of JSON objects of all the linked activities.
        """

        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_activities"])

        return jsonify(ActivitiesModel.get_collection_activities(collection, type_name=type_name))


@ns.route('/<int:activity_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityResource(Resource):
    """
    This is a specific activity resource endpoint.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, activity_id):  # pylint: disable=no-self-use
        """
        Get the activity with the given activity id.
        - __:param *collection_id*:__ The id of the collection the activity belongs to.
        - __:param *activity_id*:__ The id of the activity to get.
        - __:return:__ A JSON object of the requested activity.
        """
        activity = md.Activity.get(activity_id, required=True)

        authorize(activity.collection, ["see_activities"])

        return jsonify(ActivitiesModel.get_activity(activity_id))

    @auth_required
    def put(self, collection_id, activity_id):
        """
        Function changing the visibility of a test.
        - __:param *collection_id*:__ The collection_id the activity is in.
        - __:param *activity_id*:__ The activity id specifying which activity should be changed.
        - __:param *visible*:__ The new visibility value.
        """
        data = request.json
        activity = md.Activity.get(activity_id, required=True)

        authorize(activity.collection, ["manage_activities"])

        return jsonify(ActivitiesModel.update_activity(activity_id, data))

    @auth_required
    def delete(self, collection_id, activity_id):
        """
        Deletes the given activity
        :param collection_id: id of the collection to which the activity is connected
        :param activity_id: id of the activity
        :return: 204
        """
        activity = md.Activity.get(activity_id, required=True)

        authorize(activity.collection, ["manage_activities"])

        ActivitiesModel.delete_activity(activity.id)

        return None, 204


@ns.route('/<int:activity_id>/mark_completed')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityCompletedResource(Resource):
    """
    This is a specific activity resource endpoint.
    """

    @auth_required
    def post(self, collection_id, activity_id):
        """
        Makes a result entry in the LRS to indicate an activity is completed
        - __:param *collection_id*:__ The collection_id the activity is in.
        - __:param *activity_id*:__ The activity id specifying which activity should be changed.
        """
        data = request.json
        activity = md.Activity.get(activity_id, required=True)

        authorize(activity.collection, ["see_activities"])

        return ActivitiesModel.mark_as_completed(activity.collection, activity_id, data)


@ns.route('/<int:activity_id>/mark_started')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityStartedResource(Resource):
    """
    This is a specific activity resource endpoint.
    """

    @auth_required
    def post(self, collection_id, activity_id):
        """
        Makes a result entry in the LRS to indicate the user has started the activity
        - __:param *collection_id*:__ The collection_id the activity is in.
        - __:param *activity_id*:__ The activity id specifying which activity should be changed.
        """
        data = request.json
        activity = md.Activity.get(activity_id, required=True)

        authorize(activity.collection, ["see_activities"])

        return ActivitiesModel.mark_as_started(activity.collection, activity_id, data)


@ns.route('/<int:activity_id>/void/<string:statement_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityVoidStatementResource(Resource):
    """
    This is a specific activity resource endpoint.
    """

    @auth_required
    def post(self, collection_id, activity_id, statement_id):
        """
        Makes a result entry in the LRS to indicate the user has marked the activity as unseen
        - __:param *collection_id*:__ The collection_id the activity is in.
        - __:param *activity_id*:__ The activity id specifying which activity should be changed.
        """
        activity = md.Activity.get(activity_id, required=True)

        authorize(activity.collection, ["see_activities"])

        return ActivitiesModel.void_statement(activity.collection, activity_id, statement_id)


@ns.route('/give_response')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityResponseResource(Resource):
    """
    This is a specific activity resource endpoint.
    """

    @auth_required
    def post(self, collection_id):
        """
        Makes a result entry in the LRS to indicate an activity is completed
        - __:param *collection_id*:__ The collection_id the activity is in.
        - __:param *activity_id*:__ The activity id specifying which activity should be changed.
        - __:param *visible*:__ The new visibility value.
        """
        data = request.json
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_activities"])

        return ActivitiesModel.give_reponse(collection, data)


@ns.route('/<int:activity_id>/attachments')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityAttachmentsResource(Resource):
    """
    This is a specific activity resource endpoint.
    """

    @auth_required
    def post(self, collection_id, activity_id):
        """
        Adds the attached file to the attachments of the given activity
        - __:param *collection_id*:__ The collection_id the activity is in.
        - __:param *activity_id*:__ The activity id specifying which activity should be changed.
        """
        activity = md.Activity.get(activity_id, required=True)
        authorize(activity.collection, ["manage_activities"])

        metadata = request.form.get("test_info")
        print(f"Content\n{metadata}")
        files = request.files.getlist("files")

        return jsonify(ActivitiesModel.add_attachments(activity_id, files))


@ns.route('/attachment/<string:attachment_uu_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityAttachmentResource(Resource):
    """
    This is a specific activity resource endpoint.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, attachment_uu_id):  # pylint: disable=no-self-use
        """
        Get the activity with the given activity id.
        - __:param *collection_id*:__ The id of the collection the activity belongs to.
        - __:param *activity_id*:__ The id of the activity to get.
        - __:return:__ A JSON object of the requested activity.
        """
        attachment = md.ActivityAttachment.get(attachment_uu_id, required=True)

        authorize(attachment.activity.collection, ["see_activities"])

        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'],
            str(attachment.uuid),
            as_attachment=True,
            attachment_filename=attachment.filename)

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id, attachment_uu_id):  # pylint: disable=no-self-use
        """
        Get the activity with the given activity id.
        - __:param *collection_id*:__ The id of the collection the activity belongs to.
        - __:param *activity_id*:__ The id of the activity to get.
        - __:return:__ A JSON object of the requested activity.
        """
        attachment = md.ActivityAttachment.get(attachment_uu_id, required=True)

        authorize(attachment.activity.collection, ["manage_activities"])

        return ActivitiesModel.delete_attachment(attachment)


@ns.route('/connect/<int:head_activity_id>/<int:tail_activity_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityRelationResource(Resource):
    """
    This is a specific activity resource endpoint.
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id, head_activity_id, tail_activity_id):  # pylint: disable=no-self-use
        """
        Get the activity with the given activity id.
        - __:param *collection_id*:__ The id of the collection the activity belongs to.
        - __:param *activity_id*:__ The id of the activity to get.
        - __:return:__ A JSON object of the requested activity.
        """
        head_activity = md.Activity.get(head_activity_id, required=True)

        authorize(head_activity.collection, ["see_activities"])

        data = request.json
        return ActivitiesModel.connect_activities(
            head_activity_id=head_activity_id,
            tail_activity_id=tail_activity_id,
            type_id=data["type_id"],
            properties=data.get("properties", {})
        ), 201

    @auth_required
    def put(self, collection_id, head_activity_id, tail_activity_id):
        """
        Function changing the visibility of a test.
        - __:param *collection_id*:__ The collection_id the activity is in.
        - __:param *activity_id*:__ The activity id specifying which activity should be changed.
        - __:param *visible*:__ The new visibility value.
        """
        data = request.json
        head_activity = md.Activity.get(head_activity_id, required=True)

        authorize(head_activity.collection, ["manage_activities"])

        return jsonify(ActivitiesModel.update_activity_connection(
            head_activity_id=head_activity_id,
            tail_activity_id=tail_activity_id,
            type_id=data.get("type_id", None),
            properties=data.get("properties", None)
        ))

    @auth_required
    def delete(self, collection_id, head_activity_id, tail_activity_id):
        """
        Deletes the given activity
        :param collection_id: id of the collection to which the activity is connected
        :param activity_id: id of the activity
        :return: 204
        """
        head_activity = md.Activity.get(head_activity_id, required=True)

        authorize(head_activity.collection, ["manage_activities"])

        ActivitiesModel.delete_activity_connection(head_activity_id=head_activity_id, tail_activity_id=tail_activity_id)

        return None, 204

@ns.route('/<int:activity_id>/loadresults')
@ns.doc(params={"collection_id": "The id of the collection",
                "activity_id": "The id of the activity"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityLoadResults(Resource):
    """
    This will load the results of the activity from the external source designated in the database.
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id, activity_id):  # pylint: disable=no-self-use, unused-argument
        """
        Load the results of the activity from the external source designated in the database
        - __:param *collection_id*:__ The id of the collection to get the results from
        - __:param *activity_id*:__ The id of the activity to get the results for
        - __:return:__ A JSON object of the specified activity.
        """
        activity = md.Activity.get(activity_id, required=True)

        if authorize(activity.collection, ["load_activity_results"]):
            return activity.load_result(activity_id)


@ns.route('/<int:activity_id>/load_candidates')
@ns.doc(params={"collection_id": "The id of the collection",
                "activity_id": "The id of the activity"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityLoadCandidates(Resource):
    """
    This will load the results of the activity from the external source designated in the database.
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id, activity_id):  # pylint: disable=no-self-use, unused-argument
        """
        Load the results of the activity from the external source designated in the database
        - __:param *collection_id*:__ The id of the collection to get the results from
        - __:param *activity_id*:__ The id of the activity to get the results for
        - __:return:__ A JSON object of the specified activity.
        """
        activity = md.Activity.get(activity_id, required=True)

        if authorize(activity.collection, ["load_activity_results"]):
            return activity.load_candidates(activity_id)


@ns.route('/correlation')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityCorrelation(Resource):
    """
    This will load the results of the activity from the external source designated in the database.
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Load the results of the activity from the external source designated in the database
        - __:param *collection_id*:__ The id of the collection to get the results from
        - __:param *activity_id*:__ The id of the activity to get the results for
        - __:return:__ A JSON object of the specified activity.
        """
        data = request.json
        collection = Collection.get(collection_id, required=True)

        if authorize(collection, ["load_activity_results"]):
            return calculate_inter_item_correlation(collection, data)


@ns.route('/rir')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityRir(Resource):
    """
    This will load the results of the activity from the external source designated in the database.
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Load the results of the activity from the external source designated in the database
        - __:param *collection_id*:__ The id of the collection to get the results from
        - __:param *activity_id*:__ The id of the activity to get the results for
        - __:return:__ A JSON object of the specified activity.
        """
        data = request.json
        collection = Collection.get(collection_id, required=True)

        if authorize(collection, ["load_activity_results"]):
            return calculate_rir_value(collection, data)


@ns.route('/invalidate')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityInvalidate(Resource):
    """
    This will load the results of the activity from the external source designated in the database.
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Load the results of the activity from the external source designated in the database
        - __:param *collection_id*:__ The id of the collection to get the results from
        - __:param *activity_id*:__ The id of the activity to get the results for
        - __:return:__ A JSON object of the specified activity.
        """
        collection = Collection.get(collection_id, required=True)

        if authorize(collection, ["load_activity_results"]):
            for activity in collection.activities:
                average_grade(activity.id)
                average_duration(activity.id)
                update_question_properties(activity.id)


@ns.route('/statements/download')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityDownload(Resource):
    """
    This will load the results of the activity from the external source designated in the database.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Load the results of the activity from the external source designated in the database
        - __:param *collection_id*:__ The id of the collection to get the results from
        - __:param *activity_id*:__ The id of the activity to get the results for
        - __:return:__ A JSON object of the specified activity.
        """
        collection = Collection.get(collection_id, required=True)

        if authorize(collection, ["see_usage_report"], do_abort=False):
            student_role = Role.get_name("student", required=True)
            users = User.query.join(UserRole).filter(UserRole.role_id == student_role.id).all()
        else:
            authorize(collection, ["see_own_results"])
            users = [current_identity()]

        data = request.json
        if data is None:
            data = {}

        statements = ActivitiesModel.get_user_statements(collection, users, data.get("format", "json"))

        if data.get("format", "json") == "json":
            return statements
        elif data.get("format", "json") == "csv":
            response = Response(
                statements,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename=statements.csv"})
            return response


@ns.route('/<int:activity_id>/results/download')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ActivityResultsDownload(Resource):
    """
    This will load the results of the activity from the external source designated in the database.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, activity_id):  # pylint: disable=no-self-use, unused-argument
        """
        Load the results of the activity from the external source designated in the database
        - __:param *collection_id*:__ The id of the collection to get the results from
        - __:param *activity_id*:__ The id of the activity to get the results for
        - __:return:__ A JSON object of the specified activity.
        """
        collection = Collection.get(collection_id, required=True)

        if authorize(collection, ["see_usage_report"], do_abort=False):
            student_role = Role.get_name("student", required=True)
            users = User.query.join(UserRole).filter(UserRole.role_id == student_role.id).all()
        else:
            authorize(collection, ["see_own_results"])
            users = [current_identity()]

        data = request.json
        if data is None:
            data = {}

        result = ActivitiesModel.export_activity_responses(collection, activity_id, users)

        return Response(
            result,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=statements.csv"}
        )
