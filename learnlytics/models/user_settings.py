"""
This module contains classes with function for retrieving and saving user settings
"""

import json
from threading import Lock

from learnlytics.database.usersettings.usersettings import UserSettings
import learnlytics.database.studydata as md
from learnlytics.extensions import db

lock = Lock()


# pylint: disable=no-member
class CourseUserSettings(object):  # pylint: disable=no-init
    """
    The class contains methods called by the user settings resource.
    """

    @staticmethod
    def upsert_user_settings(user, preferences):  # pylint: disable=too-many-arguments
        """
        Adds a new user preference to the user_settings table or overwrites an already existing user setting.
        :param user: The current user
        :param course_id: The id of the current course
        :param preferences: Dictionary representing the preferences
        :return: 404 or nothing
        """
        with lock:
            entry = UserSettings.query.filter(
                UserSettings.user_id == user.id).one_or_none()

            if entry is not None:
                result = json.loads(entry.preferences)

                current_keys = [key for (key, value) in result.items()]
                for key, value in preferences.items():
                    if type(value) is dict and key in current_keys:
                        for val_key, val_value in value.items():
                            result[key][val_key] = val_value
                    else:
                        result[key] = value

                new_preferences = json.dumps(result)

                entry.preferences = new_preferences
                result = new_preferences
            else:
                result = json.dumps(preferences)
                setting = UserSettings(user_id=user.id, preferences=result)
                db.session.add(setting)

            db.session.commit()
            return json.loads(result)

    @staticmethod
    def get_user_settings(user_id):  # pylint: disable=too-many-arguments
        """
        Gets the list of all user settings
        :param user: The current user
        :param course_id: The id of the current course
        :return: A JSON of the user's preferences
        """
        result = UserSettings.query.filter(UserSettings.user_id == user_id).one_or_none()

        if result is None:
            return {}

        return json.loads(result.preferences)

    @staticmethod
    def get_user_persons(user_id):
        persons = md.Person.query.filter(md.Person.user_id == user_id)
        person_dict = []
        for person in persons:
            person_dict.append({
                "display_name": person.display_name,
                "mail": person.mail,
                "institution_id": person.institution_id,
                "remote_id": person.remote_id,
                "lrs_actor": person.lrs_actor
            })

        return person_dict
