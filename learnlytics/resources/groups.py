# coding=utf-8
"""
This module contains all the endpoints for getting the users associated to a collection.
"""
from flask import request
from flask_restplus import Resource, abort

from create_api import groupsns as ns
from learnlytics.authentication import auth_required, current_identity
from learnlytics.authorization.manager import authorize, add_collection, remove_collection, change_collection
from learnlytics.database.authorization.collection import Collection
from learnlytics.models.collection import Collections as CollectionsModel
from learnlytics.models.users import UsersModel


@ns.route('/')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionGroups(Resource):
    """
    Overview of all student entities of a collection
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Gets all groups that are part of the collection
        - __:param *collection_id*:__ The id of the collection
        - __:return:__ A dictionary of all relevant student entity information:
        ```
        ```
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_collection"])

        return CollectionsModel.get_collection(collection_id)["subcollections"]

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id):  # pylint: disable=no-self-use, unused-argument
        """
        Adds the students listed in the attach csv file to the given collection
        - __:param *collection_id*:__ The id of the collection
        """
        collection = Collection.get(collection_id, required=True)
        authorize(collection, ["manage_collection"])

        data = request.get_json()
        name = data.get("name")

        group = add_collection(name, parent_id=collection_id)
        UsersModel.add_users_to_group(group.id, [{
            "id": current_identity().id,
            "roles": ["admin"]
        }])

        return CollectionsModel.get_collection(group.id)


@ns.route('/<int:group_id>')
@ns.doc(params={"collection_id": "The id of the collection",
                "user_id": "The id of the student"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionGroup(Resource):
    """
    Details of a student entity
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, group_id):  # pylint: disable=no-self-use, unused-argument
        """
        Gets the details of a single group entity
        - __:param *collection_id*:__ The id of the collection
        - __:param *group_id*:__ The id of the the group
        - __:return:__ A dictionary of all relevant student entity information:
        ```
        ```
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_collection"])
        if group_id not in [group.id for group in collection.children]:
            abort(400, "The given group id does not match the collection id")

        return CollectionsModel.get_collection(group_id)

    @auth_required
    @ns.response(200, 'Success')
    def put(self, collection_id, group_id):  # pylint: disable=no-self-use, unused-argument
        """
        Change the details of a single group entity
        - __:param *collection_id*:__ The id of the collection
        - __:param *group_id*:__ The id of the the group
        - __:return:__ A dictionary of all relevant student entity information:
        ```
        ```
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["manage_collection"])
        if group_id not in [group.id for group in collection.children]:
            abort(400, "The given group id does not match the collection id")

        try:
            data = request.get_json()
            group = Collection.get(group_id, required=True)
            change_collection(group, data)
            return CollectionsModel.get_collection(group_id)
        except KeyError:
            abort(400, "Collection instance does not have all attributes")

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id, group_id):  # pylint: disable=no-self-use, unused-argument
        """
        Delete a single group entity
        - __:param *collection_id*:__ The id of the collection
        - __:param *group_id*:__ The id of the the group
        - __:return:__ A dictionary of all relevant student entity information:
        ```
        ```
        """
        collection = Collection.get(collection_id, required=True)
        group = Collection.get(group_id, required=True)

        authorize(group, ["manage_collection"])
        if group_id not in [group.id for group in collection.children]:
            abort(400, "The given group id does not match the collection id")

        remove_collection(group)

        return None, 204


@ns.route('/<int:group_id>/users')
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
    def post(self, collection_id, group_id):  # pylint: disable=no-self-use, unused-argument
        """
        Adds students to the group
        - __:param *collection_id*:__ The id of the collection
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["manage_collection"])
        if group_id not in [group.id for group in collection.children]:
            abort(400, "The given group id does not match the collection id")

        data = request.json
        if not isinstance(data, list):
            data = [data]

        UsersModel.add_users_to_group(group_id, data)
        user_ids = [user_data["id"] for user_data in data]
        return UsersModel.get_collection_users(group_id, user_ids), 201


@ns.route('/<int:group_id>/users/<int:user_id>')
@ns.doc(params={"collection_id": "The id of the collection"})
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionUser(Resource):
    """
    Overview of all student entities of a collection
    """

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id, group_id, user_id):  # pylint: disable=no-self-use, unused-argument
        """
        Delete students from the group
        - __:param *collection_id*:__ The id of the collection
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["manage_collection"])
        if group_id not in [group.id for group in collection.children]:
            abort(400, "The given group id does not match the collection id")

        UsersModel.delete_users_from_group(group_id, [user_id])
        return None, 204
