# coding=utf-8
"""
This module contains all the endpoints for getting the users associated to a collection.
"""

import json

from io import StringIO
from flask import request
from flask_restplus import Resource, marshal, marshal_with, fields, abort

from create_api import usersns as ns
from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize
from learnlytics.connectors.csv_import.new_users import add_new_users
from learnlytics.models.users import UsersModel
from learnlytics.database.authorization.collection import Collection


@ns.route('/')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionUsers(Resource):
    """
    Overview of all student entities of a collection
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Gets all students that follow the collection
        - __:param *collection_id*:__ The id of the collection
        - __:return:__ A dictionary of all relevant student entity information:
        ```
        ```
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_users"])

        return UsersModel.get_collection_all_users(collection_id)

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Adds the students listed in the attach csv file to the given collection
        - __:param *collection_id*:__ The id of the collection
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["manage_users"])
        if request.content_type.startswith("application/json"):
            data = request.json
            UsersModel.new_user(collection_id, data)

            return True, 201
        elif request.content_type.startswith("multipart/form-data"):
            files = request.files
            file = StringIO(files["file"].stream.read().decode("utf-8"))

            add_new_users(file, collection_id)

            return True, 201

        return "Content type not supported", 400


@ns.route('/<int:user_id>')
@ns.doc(params={"collection_id": "The id of the collection",
                "user_id": "The id of the student"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionUser(Resource):
    """
    Details of a student entity
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, user_id):  # pylint: disable=no-self-use, unused-argument
        """
        Gets the details of a single student entity
        - __:param *collection_id*:__ The id of the collection
        - __:param *student_id*:__ The id of the the student
        - __:return:__ A dictionary of all relevant student entity information:
        ```
        ```
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_users", "see_user_results"])

        return UsersModel.get_collection_user(collection_id, user_id)


@ns.route('/<int:user_id>/results')
@ns.doc(params={
    "collection_id": "The id of the collection",
    "user_id": "The id of the student"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionUserResults(Resource):
    """
    Details of a student entity
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, user_id):  # pylint: disable=no-self-use, unused-argument
        """
        Gets the details of a single student entity
        - __:param *collection_id*:__ The id of the collection
        - __:param *student_id*:__ The id of the the student
        - __:return:__ A dictionary of all relevant student entity information:
        ```
        ```
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_users", "see_user_results"])

        return UsersModel.get_results_for_user(collection, user_id)


@ns.route('/<int:user_id>/persons')
@ns.doc(params={
    "collection_id": "The id of the collection",
    "user_id": "The id of the student"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionUserResults(Resource):
    """
    Details of a student entity
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, user_id):  # pylint: disable=no-self-use, unused-argument
        """
        Gets the details of a single student entity
        - __:param *collection_id*:__ The id of the collection
        - __:param *student_id*:__ The id of the the student
        - __:return:__ A dictionary of all relevant student entity information:
        ```
        ```
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_users", "see_user_results"])

        return UsersModel.get_results_for_user(collection, user_id)


@ns.route('/students/anonymize')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class StudentAnonymize(Resource):
    """
    Details of a student entity
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Anonymizes all users with a student role by assign a new random name, email and password. Student ID is not
        changed at the moment this must be done during instantiation of the database
        see /Scripts/anonymize_student_ids.py
        """
        import names
        import random
        from learnlytics.database.authorization.collection import Collection
        from learnlytics.database.authorization.role import Role
        from learnlytics.database.authorization.user import User, UserRole, UserPassHash
        if authorize(Collection.get_root_collection(required=True), ["use_dev_calls"]):
            student_role = Role.get_name("student", required=True)
            students = User.query.join(UserRole).filter(UserRole.role_id == student_role.id).all()

            gen_names = []
            gen_first_names = []
            gen_last_names = []
            while len(gen_names) < len(students):
                first_name = names.get_first_name()
                last_name = names.get_last_name()
                name = first_name + " " + last_name
                if name not in gen_names:
                    gen_names.append(name)
                    gen_first_names.append(first_name)
                    gen_last_names.append(last_name)

            i = 0
            for student in students:
                student.first_name = gen_first_names[i]
                student.last_name = gen_last_names[i]
                student.display_name = student.first_name + " " + student.last_name
                student.mail = student.first_name.lower() + "." + student.last_name.lower() + "@learnlytics.uu.nl"
                student.institution_id = str(random.randint(1000000, 9999999))

                i += 1
                pass_hash = UserPassHash.query.get(student.id)
                pass_hash.reset_password("test")

                for person in student.persons:
                    person.person_name = student.display_name
                    person.display_name = student.display_name
                    person.mail = student.mail
                    person.institution_id = student.institution_id


@ns.route('/invalidate')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class UserInvalidate(Resource):
    """
    Invalidation
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        This will add the lrs actor to persons that are missing them in this collection
        """
        from learnlytics.extensions import db

        if authorize(Collection.get_root_collection(required=True), ["use_dev_calls"]):
            collection = Collection.get(collection_id, required=True)

            for user in collection.all_users:
                for person in user.persons:
                    person.lrs_actor = str(person.get_lrs_actor())

            db.session.commit()
