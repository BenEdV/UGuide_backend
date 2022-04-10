from flask import request
from flask_restplus import Resource, abort
from sqlalchemy.exc import IntegrityError

from create_api import api_exams_ns as ns
from learnlytics.api.models.authentication import authenticate
from learnlytics.api.models.authorization import authorize_gen_api
from learnlytics.api.models.exams import Exams as ExamModel
from learnlytics.api.models.result_model import Result
from learnlytics.api.restplus_models.expect_models import post_exams_fields, post_exam_results_fields


@ns.route('/')
@ns.response(201, 'Created')
@ns.response(409, 'Integrity Error')
class AddExamsResource(Resource):
    """
    The resource used to add exams
    """
    exam_model = ExamModel(forced=True)

    @ns.expect(post_exams_fields)
    def post(self):
        """
        Add exams
        - __:return:__ True
        - __:param *request_data*__: Optional request_data for internal connector use.
        """
        key = authenticate()
        data = request.get_json()

        exams = data.get("exams")
        collection_id = data.get("collection_id")

        authorize_gen_api(key, collection_id, ["add_exam"])

        if not exams:
            abort(400, message="No exams provided")
        for exam in data["exams"]:
            exam = self.exam_model.add_exam(collection_id, exam, key.requester)
        return exam.id, 201


@ns.route('/forced')
class ForceAddExamsResource(AddExamsResource):
    """
    Delete the existing entry if it exists before adding the new entry
    """
    exam_model = ExamModel(forced=True)


@ns.route('/<activity_id>/results')
@ns.response(201, 'Added results to exams')
class AddExamResultsResource(Resource):
    """
    The resource used to add examresults
    """

    # @ns.expect(post_exam_results_fields)
    def post(self, activity_id):
        """
        Add exam results
        - __:return:__ True
        - __:param activity_id__: The activity_id of the exam of which the results should be added to
        - __:param *request_data*__: Optional request_data for internal connector use.
        """
        key = authenticate()
        data = request.get_json()

        import learnlytics.database.studydata as md

        exam = md.Activity.get(activity_id, required=True)
        if exam.type.name != "exam":
            abort(400, message="The activity with the given id is not an exam")
        authorize_gen_api(key, exam.collection.id, ["add_exam_result"])

        examresults = data.get("exam_results")
        if not examresults:
            abort(400, message="No results provided")

        Result.add_results(examresults, exam, key.requester)
        return True, 201


@ns.route('/results/forced')
class ForceAddExamResultsResource(AddExamResultsResource):
    """Delete the existing entry if it exists before adding the new entry"""
    exam_model = ExamModel(forced=True)
