"""
    This file contains flask restful resources for administration purposes on the authorization system
"""

import inspect
from flask import current_app, request
from flask_restplus import Resource, marshal, marshal_with_field, marshal_with, fields, abort
from sqlalchemy import and_

from create_api import authorizationns as ns

from learnlytics.authentication import auth_required
from learnlytics.authentication.util import current_identity
from learnlytics.authorization.manager import authorize, get_users_with_role, get_collection_hierarchy, \
    remove_collection, add_collection, change_collection, add_role, remove_role, change_role, get_user_roles
import learnlytics.authorization.manager as auth
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.permission import Permission
from learnlytics.database.authorization.role import Role
from learnlytics.database.authorization.user import User
from learnlytics.models.collection import Collections as CollectionsModel
from learnlytics.resources.restplus_models.expect_models import post_fields,\
    authorization_user_permission_post_fields, authorization_roles_post_fields


# pylint: disable= no-self-use
@ns.route("/collection/")
@ns.response(401, 'Unauthorized')
class CollectionsResource(Resource):
    """
    Resource exposing a function that returns hierarchy in dictionary form and info on the collections through get
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):
        """
        Function returning the authorisation hierarchy in dictionary form.
        - __:return:__ Dictionary of the authorisation hierarchy tree.
        """
        return CollectionsModel.get_collections()

    @auth_required
    @ns.response(200, 'Success')
    def post(self):
        """
        Function returning the authorisation hierarchy in dictionary form.
        - __:return:__ Dictionary of the authorisation hierarchy tree.
        """
        data = request.get_json()

        if not isinstance(data, list):
            data = [data]

        collections = []
        for collection_data in data:
            parent_id = collection_data.get("parent_id", 1)
            name = collection_data.get("name")
            parent = Collection.get(parent_id, required=True)
            authorize(parent, ["manage_collection"])

            collection = add_collection(name, parent_id=parent_id)
            collections.append(CollectionsModel.get_collection(collection.id))

            user_roles = get_user_roles(parent_id)
            for role in user_roles:
                auth.add_user_role(current_identity().id, role.id, collection.id)

        return collections


@ns.route("/collection/<collection_id>")
@ns.doc(params={"collection_id": "Id of the authorization collection"})
@ns.response(401, 'Unauthorized')
@ns.response(400, 'Bad Request')
@ns.response(404, 'Not Found')
class CollectionResource(Resource):
    """
    Resource exposing an endpoint for collections.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):
        """
        Function that gets info about a collection object
        - __:param *collection_id*:__ The id of the collection.
        - __:return:__ A Json object of the collection object.
        """
        collection = Collection.get(collection_id, required=True)
        authorize(collection, ["see_collection"])
        return CollectionsModel.get_collection(collection_id)

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id):
        """
        Function deleting a collection
        - __:param *collection_id*:__ The id of the collection to delete.
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["manage_collection"])
        remove_collection(collection)

        return None, 204

    @auth_required
    @ns.response(200, 'Success')
    @ns.expect(post_fields)
    def put(self, collection_id):
        """
        Function changing attributes of a collection.
        Attributes to be changed should be in the put body like a
        dictionary, it ignores unknown keys.
        - __:param *collection_id*:__ The id of the collection.
        """
        collection = Collection.get(collection_id, required=True)
        authorize(collection, ["manage_collection"])
        try:
            data = request.get_json()
            updated_collection = change_collection(collection, data)
            return CollectionsModel.get_collection(updated_collection.id)
        except KeyError:
            abort(400, "Collection instance does not have all attributes")


@ns.route("/roles/<role_id>")
@ns.doc(params={"role_id": "Id of the role"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class RoleResource(Resource):
    """
    Resource exposing an endpoint for Roles
    """

    _get_fields = {
        "name": fields.String,
        "permissions": fields.List(fields.String)
    }

    @auth_required
    @ns.response(200, 'Success')
    @marshal_with(_get_fields)
    def get(self, role_id):
        """
        Function that gets info about a role object
        - __:param *collection_id*:__ The id of the collection the role belongs to.
        - __:param *role_id*:__ The name of the role object.
        - __:return:__ marshaled collection object.
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["see_roles"])
        role = Role.get(role_id, required=True)

        return role

    @auth_required
    @ns.response(201, 'Created')
    @ns.expect(authorization_roles_post_fields)
    def post(self, role_id):
        """
        Function that adds new a new role on the collection.
        - __:param *collection_id*:__ The id of the collection the role belongs to.
        - __:param *role_id*:__ The name of the role to be added.
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["manage_roles"])
        data = request.get_json()
        add_role(role_id, data["permissions"])
        return 200

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, role_id):
        """
        Function deleting a role.
        - __:param *collection_id*:__ The id of the collection the role belongs to.
        - __:param *role_id*:__ The name of the role.
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["manage_roles"])
        role = Role.get(role_id, required=True)
        remove_role(role)

        return None, 204

    @auth_required
    @ns.response(200, 'Success')
    def put(self, role_id):
        """
        Function changing attributes of a role.
        - __:param *collection_id*:__ The id of the collection.
        - __:param *role_id*:__ The name of the role.
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["manage_roles"])
        role = Role.get(role_id, required=True)

        data = request.get_json()
        change_role(role, data["permissions"])

        return None, 204


@ns.route("/<int:collection_id>/user_role/<int:user_id>/<int:role_id>")
@ns.doc(params={"collection_id": "Id of the authorization collection",
                "user_id": "Id of the user"})
# pylint: disable= no-self-use
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionUserRole(Resource):
    """
    Resource for adding and removing user roles
    """

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id, user_id, role_id):
        """
        Gives the user the role for the collection
        - __:param *collection_id*:__ The id of the collection.
        - __:param *user_id*:__ The id of the user.
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["manage_collection_user_roles"])

        auth.add_user_role(user_id, role_id, collection_id)

        return True, 201

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id, user_id, role_id):
        """
        Removes the role of the user for the collection
        - __:param *collection_id*:__ The id of the collection.
        - __:param *user_id*:__ The id of the user.
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["manage_collection_user_roles"])

        auth.remove_user_role(user_id, role_id, collection_id)

        return None, 204


@ns.route("/collection/<int:collection_id>/permissions")
@ns.doc(params={"collection_id": "Id of the authorization collection"})
# pylint: disable= no-self-use
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class CollectionUserPermissions(Resource):
    """
    Resource for getting a list of permissions current user has for given collection
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):
        """
        Gives a list of permissions that the user has for the collection
        - __:param *collection_id*:__ The id of the collection.
        """
        _ = Collection.get(collection_id, required=True)

        permissions = auth.get_user_permissions(collection_id)

        if permissions == []:
            # show a 404 if user has no permissions for given collection
            Collection.fake_404(collection_id)

        permission_names = [permission.name for permission in permissions]

        return permission_names


@ns.route("/permission/")
@ns.doc(params={"collection_id": "Id of the authorization collection"})
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class UserPermissionResource(Resource):
    """
    Resource for collection permissions
    """

    _get_fields = {"name": fields.String, "id": fields.Integer}

    @auth_required
    @ns.response(200, 'Success')
    @marshal_with_field(fields.List(fields.Nested(_get_fields)))
    def get(self):
        """
        Function that returns all users that have direct permission on that collection
        - __:param *collection_id*:__ The id of the collection.
        - __:param *permission_name*:__ the name of the permission.
        - __:return:__ A list of user_ids that have permission on the collection.
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["see_permissions"])

        return Permission.query.all()

    @auth_required
    @ns.response(201, 'Created')
    @ns.expect(authorization_user_permission_post_fields)
    def post(self):
        """
        Function that can add or remove permissions of users.
        Remove key must be set to true to remove permissions instead of adding.
        - __:param *collection_id*:__ The id of the collection.
        - __:param *permission_name*:__ The name of the permission.
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["manage_permissions"])

        data = request.get_json()
        auth.add_permissions(data["permissions"])

    @auth_required
    @ns.response(200, 'Success')
    def delete(self):
        """
        Function that can remove the permission object on the collection.
        """
        root = Collection.get_root_collection(required=True)
        authorize(root, ["manage_permissions"])

        data = request.get_json()
        auth.delete_permissions(data["permissions"])

        return None, 204
