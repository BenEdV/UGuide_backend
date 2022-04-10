"""
This module contains all the endpoints for courses.
"""

from flask import request
from flask_restplus import Resource, fields, marshal_with, abort, marshal

from create_api import course_instances_ns as ns
from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize, get_users_with_role
from learnlytics.database.authorization.collection import Collection
from learnlytics.models.course_instances import CourseInstances as CourseInstancesModel
import learnlytics.database.studydata as md


@ns.route('/')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CourseInstancesResource(Resource):
    """
    This class is the resource endpoint for all courses.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Gets a list of all available courses.
        - __:return:__ a list of json objects of all the available courses.

        """

        result_dic = CourseInstancesModel.get_course_instances()
        return result_dic

    post_course_instance_fields = ns.model("Course", {
        "parent_collection_id": fields.Integer(required=False, example=2, description="id of parent Collection"),
        "collection_id": fields.Integer(required=False, example=2, description="id of Collection"),
        "course_id": fields.Integer(required=True, example=3),
        "period_id": fields.Integer(example=2, description="id of Period"),
    })

    @auth_required
    @ns.response(201, 'Created')
    @ns.expect(post_course_instance_fields, validate=True)
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

        course_instances = []
        for course_instance_data in data:
            if "parent_collection_id" not in course_instance_data and "collection_id" not in course_instance_data:
                abort(400, (
                    "Please provide a parent_collection_id to create a new collection as child of the parent, "
                    "or provide the collection_id of an exisiting collection to link a course to that collection"
                ))

            collection = None

            if "parent_collection_id" in course_instance_data:
                parent_collection = Collection.get(course_instance_data["parent_collection_id"], required=True)

                authorize(parent_collection, ["manage_collection"])

            elif "collection_id" in course_instance_data:
                collection = Collection.get(course_instance_data["collection_id"], required=True)

                authorize(collection, ["manage_collection"])

            course_instance = CourseInstancesModel.add_course_instance(
                course_id=course_instance_data["course_id"],
                period_id=course_instance_data["period_id"],
                parent_collection_id=course_instance_data.get("parent_collection_id", None),
                collection=collection
            )

            course_instances.append(course_instance)

        return course_instances


@ns.route('/<int:course_instance_id>')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
@ns.doc(params={"course_id": "The id of the course"})
class CourseInstanceResource(Resource):
    """
    This class is the resource endpoint for a single course.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, course_instance_id):  # pylint: disable=no-self-use
        """
        Gets a course instance with the given course_instance_id.
        - __:param *course_instance_id*__: id of the course instance to get.
        - __:return__: a json object of the requested course instance.
        """
        course_instance = md.CourseInstance.get(course_instance_id, required=True)

        authorize(course_instance.collection, ["see_collection"])

        return CourseInstancesModel.get_course_instance(course_instance_id)

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, course_instance_id):  # pylint: disable=no-self-use
        """
        Deletes a course with the given course_id.
        - __:param *course_id*__: The id of the course to delete.
        - __:return__: True
        """
        course_instance = md.CourseInstance.get(course_instance_id, required=True)

        authorize(course_instance.collection, ["manage_collection"])

        CourseInstancesModel.delete_course_instance(course_instance)

        return None, 204
