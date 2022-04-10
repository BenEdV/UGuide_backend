"""
This module contains the model for collections
"""

from learnlytics.authentication.util import current_identity
import learnlytics.authorization.manager as auth
from learnlytics.database.authorization.collection import Collection, UserCollectionSettings
from learnlytics.database.authorization.permission import Permission
from learnlytics.database.authorization.role import RolePermission
from learnlytics.database.authorization.user import UserRole
from learnlytics.extensions import db


# pylint: disable=no-member
class Collections(object):  # pylint: disable=no-init
    """
    This class contains methods to get, add delete collections
    """

    @staticmethod
    def get_collection(collection_id):
        """
        Gets a collection with the given collection_id.
        :param collection_id: id of the the collection to get
        :return: a json of the requested collection.
        """
        collection = Collection.get(collection_id, required=True)
        result_dic = Collections._collection_dict(collection)

        for child_collection in collection.children:
            result_dic["subcollections"].append({"id": child_collection.id})

        return result_dic

    @staticmethod
    def _collection_dict(collection):
        permissions = auth.get_user_permissions(collection.id)
        permission_names = [permission.name for permission in permissions]

        user_roles = current_identity().roles_for_collection(collection.id)

        collection_dict = {
            "id": collection.id,
            "name": collection.name,
            "permissions": permission_names,
            "course_instance_id": collection.course_instance_id,
            "settings": collection.settings,
            "logging": True,
            "roles": [role.name for role in user_roles],
            "pages": [],
            "subcollections": []
        }

        if collection.course_instance_id is not None:
            collection_dict["pages"] = [
                "overview", "module.exams", "module.models", "module.constructs", "module.study_material",
                "module.groups", "module.students", "module.surveys", "privacy", "administration.container",
                "administration.course"
            ]
        else:
            collection_dict["pages"] = [
                "overview", "module.surveys", "administration.container", "administration.collections"
            ]

        if collection.id == 5:
            collection_dict["pages"].append("module.test")

        if collection.parent_id is not None:
            collection_dict["parent"] = {"id": collection.parent_id}

        if "see_activities" in permission_names:
            collection_dict["activity_count"] = collection.activities.count()

        if "see_construct_models" in permission_names:
            collection_dict["construct_model_count"] = collection.construct_models.count()

        collection_dict["member_count"] = collection.member_count

        if "see_connectors" in permission_names:
            collection_dict["connectors_count"] = collection.connectors.count()

        user_settings = UserCollectionSettings.query.filter(
            UserCollectionSettings.collection_id == collection.id,
            UserCollectionSettings.user_id == current_identity().id).one_or_none()

        if user_settings is not None:
            collection_dict["user_settings"] = user_settings.settings
        else:
            collection_dict["user_settings"] = {}

        return collection_dict

    @staticmethod
    def get_collections():
        """
        Gets a list of all available collections.
        :return: a list of json objects of all the available collections.
        """
        # collection_tuples = db.session.query(Collection, Collection.id).all()
        collection_tuples = db.session.query(Collection, Collection.id).\
            join(UserRole, UserRole.collection_id == Collection.id).\
            filter(UserRole.user_id == current_identity().id).\
            join(RolePermission, RolePermission.role_id == UserRole.role_id).\
            join(Permission, Permission.id == RolePermission.permission_id).\
            filter(Permission.name == "see_collection").all()
        result = []
        collections = []
        collection_ids = []
        collection_dicts = {}
        for collection, collection_id in collection_tuples:
            collections.append(collection)
            collection_ids.append(collection_id)
            collection_dicts[collection.id] = Collections._collection_dict(collection)

        for collection in collections:
            collection_dict = collection_dicts[collection.id]
            if collection.parent_id in collection_ids:
                collection_dicts[collection.parent_id]["subcollections"].append({"id": collection_dict["id"]})

            result.append(collection_dict)

        return result
