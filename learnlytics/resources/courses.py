"""
This module contains all the endpoints for courses.
"""

from flask import request
from flask_restplus import Resource, fields, marshal_with, abort, marshal

from create_api import coursesns as ns
from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize, get_users_with_role
from learnlytics.database.authorization.collection import Collection
from learnlytics.models.courses import Courses as CoursesModel
import learnlytics.database.studydata as md
# from learnlytics.resources.restplus_models.expect_models import post_course_fields

id_fields_course = {
    "id": fields.Integer,
    "name": fields.String,
    "code": fields.String
}


@ns.route('/')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CoursesResource(Resource):
    """
    This class is the resource endpoint for all courses.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Gets a list of all available courses.
        - __:return:__ a list of json objects of all the available courses.
        The list has the following layout:
        ```
        return [
                  {
                    "id": 'BIOEVO'
                    "name": 'Evolutie'
                    "average": 6,
                    "participants": 60
                  },
                  {
                    "id": 'BIOPLANT'
                    "name": 'Planten'
                    "average": 6,
                    "participants": 60
                  },
                  {
                    "id": 'BIOMAM'
                    "name": 'Zoogdieren'
                    "average": 6,
                    "participants": 60
                  },
                  {
                    "id": 'BIOINSEC',
                    "name": 'Insecten'
                    "average": 6,
                    "participants": 60
                  }
                ]
        ```
        """
        if authorize(Collection.get_root_collection(required=True), ["see_all_courses"]):
            result_dic = CoursesModel.get_courses()
            return result_dic

    post_course_fields = ns.model("Course", {
        "name": fields.String(required=True, example="Biologie en ecologie van planten"),
        "code": fields.String(required=True, example="B-B1BEP13"),
    })

    @auth_required
    @ns.response(201, 'Created')
    @ns.expect(post_course_fields, validate=True)
    def post(self):  # pylint: disable=no-self-use
        """
        Adds a new course.
        - __return__: True if successful
        """
        authorize(Collection.get_root_collection(required=True), ["manage_courses"])

        # read json request data
        data = request.json

        if not isinstance(data, list):
            data = [data]

        courses = []
        for course_data in data:
            course = CoursesModel.add_course(
                name=course_data["name"],
                code=course_data["code"]
            )

            courses.append(course)

        return courses


@ns.route('/<int:course_id>')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
@ns.doc(params={"course_id": "The id of the course"})
class CourseResource(Resource):
    """
    This class is the resource endpoint for a single course.
    """

    @auth_required
    @ns.response(200, 'Success')
    @marshal_with(id_fields_course)
    def get(self, course_id):  # pylint: disable=no-self-use
        """
        Gets a course with the given course_id.
        - __:param *course_id*__: id of the course to get.
        - __:return__: a json object of the requested course.
        The json object has the following layout:
        ```
        return {
                  "id": course_id,
                  "name": 'Evolutie'
                }
        ```
        """
        course = md.Course.get(course_id, required=True)

        authorize(Collection.get_root_collection(required=True), ["see_all_courses"])

        return CoursesModel.get_course(course)

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, course_id):  # pylint: disable=no-self-use
        """
        Deletes a course with the given course_id.
        - __:param *course_id*__: The id of the course to delete.
        - __:return__: True
        """
        course = md.Course.get(course_id, required=True)

        authorize(Collection.get_root_collection(required=True), ["manage_courses"])

        CoursesModel.delete_course(course)

        return None, 204
