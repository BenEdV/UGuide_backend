"""
This module contains classes with function for retrieving and saving user settings
"""

import learnlytics.authorization.manager as auth
from learnlytics.extensions import db
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.role import Role
from learnlytics.database.authorization.user import UserPassHash, User
import learnlytics.database.studydata as md


class UsersModel(object):  # pylint: disable=no-init
    """
    Contains a methods which get users
    """

    @staticmethod
    def get_collection_user(collection_id, user_id):
        """
        Get the activity of the given collection with the given activity id
        :param activity_id: The id of the activity to get
        :return: 404 or a dictionary containing the activity data
        """
        return UsersModel.get_collection_users(collection_id, [user_id])[0]

    @staticmethod
    def get_collection_all_users(collection_id):
        """
        """
        collection = Collection.get(collection_id, required=True)
        return UsersModel.get_collection_users(collection_id, collection.all_user_ids)

    @staticmethod
    def get_collection_users(collection_id, user_ids):
        """
        Returns a list of user_ids for the ids provided
        """
        res = []

        # !!!!!!!
        # Database calls
        # !!!!!!!

        # activities
        users = User.query.filter(User.id.in_(user_ids)).all()

        if users == []:
            return []

        collection = Collection.get(collection_id)

        # !!!!!!!
        # Creating dictionary
        # !!!!!!!
        for user in users:
            group_dicts = []
            for group in collection.children:
                if user.id not in group.all_user_ids:
                    continue

                group_roles = []
                for role in user.roles_for_collection(group.id):
                    group_roles.append(role.name)

                group_dicts.append({
                  "id": group.id,
                  "roles": group_roles
                })

            roles = []
            for role in user.roles_for_collection(collection_id):
                roles.append(role.name)

            user_dict = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "display_name": user.display_name,
                "mail": user.mail,
                "institution_id": user.institution_id,
                "roles": roles,
                "groups": group_dicts
            }

            res.append(user_dict)

        # res.sort(key=lambda q: q["id"])

        return res

    @staticmethod
    def new_user(collection_id, user_data):
        user = User(
            user_data["institution_id"],
            user_data["display_name"],
            user_data["mail"],
            user_data["first_name"],
            user_data["last_name"]
        )

        db.session.add(user)
        db.session.flush()
        db.session.add(UserPassHash(
            user.id,
            user_data["password"]))

        role = Role.get_name(user_data["role"])

        auth.add_user_role(user.id, role.id, collection_id)
        db.session.commit()

    @staticmethod
    def get_results_for_user(collection, user_id):
        results = []
        lrs_connector = collection.main_lrs_connector()

        activity_id_for_lrs_id = {}
        for activity in collection.activities:
            activity_id_for_lrs_id[activity.lrs_object_id] = activity.id

        user = User.get(user_id, required=True)
        actors = [user.actor]

        for person in user.persons:
            actors.append(person.get_lrs_actor())

        params = {
            "statement.actor.account": {"$in": actors}
        }

        for statement in lrs_connector.model.get_statements(params):
            object_id = statement["object"]["id"]

            result = {
                "activity_id": activity_id_for_lrs_id[object_id],
                "verb": statement["verb"],
                "result": statement["result"],
                "timestamp": statement["timestamp"],
            }
            results.append(result)

        results.sort(key=lambda q: q["activity_id"])

        return results

    @staticmethod
    def add_users_to_group(group_id, users_data):
        for user_data in users_data:
            roles = [Role.get_name(r) for r in user_data["roles"]]
            for role in roles:
                auth.add_user_role(user_data["id"], role.id, group_id)

    @staticmethod
    def delete_users_from_group(group_id, user_ids):
        for user_id in user_ids:
            user_roles = md.UserRole.query.filter(md.UserRole.collection_id == group_id,
                                                  md.UserRole.user_id == user_id).all()
            for user_role in user_roles:
                db.session.delete(user_role)

        db.session.commit()
