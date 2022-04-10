
"""
Contains the RemindoUserModel, which handles all request related to Remindo users.
"""

from learnlytics.connectors.remindo.models import RemindoSubModel
from learnlytics.connectors.remindo.utils import time_from_string, get_recipe_id, get_moment_id


class RemindoUserModel(RemindoSubModel):
    """
    Handle all requests related to Remindo users
    """

    user_types = ["candidate", "tutor", "supervisor", "supervisor-noprofile", "checker"]

    def get_users(self, user_ids=None, user_type=None):
        """
        Leaving both parameters empty returns all Remindo users.
        Requesting user_ids returns all those users.
        Requesting a specific user_type returns all users of that type.
        The combination user_ids and user_type is not handled, since it's not expected.
        :param user_ids: ([int], optional, default None) ids of the users.
        :param user_type: (string, optional, default None) type of the users.
        :return: Remindo users.
        """
        if user_type:
            params = {"usertype": user_type}
            data = self.connector.user_list(params)
            users = []
            if data["users"]:
                for user in data["users"]:
                    users.append(self.get_user(user, user_type))
            return users

        params = {}
        if user_ids:
            params["ids"] = user_ids

        users = []
        for user_type in self.user_types:
            params["usertype"] = user_type
            data = self.connector.user_list(params)
            if data["users"]:
                for user in data["users"]:
                    users.append(self.get_user(user, user_type))
            if user_ids:
                if len(user_ids) == len(users):
                    break
        return users

    def get_candidates(self, exam):
        moment_id = get_moment_id(exam)

        candidates = self.get_moment_candidates(moment_id, full=True)

        from learnlytics.api.models.person import PersonModel
        return PersonModel.add_persons(candidates, self.code)

    def get_moment_candidate_ids(self, moment_id):
        """
        Returns the results of a moment
        :param moment_id: The id of the moment
        :return: All results of the moment
        """
        params = {"id": moment_id}
        data = self.connector.moment_list_candidates(params)
        ids = []
        for candidate in data["candidates"]:
            ids.append(candidate["user_id"])
        return ids

    def get_moment_candidates(self, moment_id, full=False):
        """
        Returns the results of a moment
        :param moment_id: The id of the moment
        :return: All results of the moment
        """
        params = {"id": moment_id}
        data = self.connector.moment_list_candidates(params)
        if full:
            user_ids = []
            for candidate in data["candidates"]:
                user_ids.append(candidate["user_id"])

            data = self.get_users(user_ids=user_ids)
            return data
        return data["candidates"]

    @staticmethod
    def get_user(user, user_type):
        """
        Cast the user to a desirable format.
        :param user: Dictionary containing user information
        :return: Remindo user
        """

        if user["linkname"] == "":
            name = user["firstname"] + " " + user["lastname"]
        else:
            name = user["firstname"] + " " + user["linkname"] + " " + user["lastname"]
        return {
            "remote_user_id": user["id"],
            "institution_id": user["username"],
            "role": user_type,
            "name": name,
            "mail": user["email"]
        }
