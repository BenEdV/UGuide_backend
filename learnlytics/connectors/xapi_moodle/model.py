# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course (3 4)
# (C) Copyright Utrecht University (Department of Information and Computing Sciences)

"""
This module contains the Moodle xapi model
"""

from learnlytics.connectors.model import ConnectorModel

from learnlytics.connectors.xapi_moodle.utils import get_object_id


class MoodleXapiModel(ConnectorModel):  # pylint: disable=too-few-public-methods
    """
    Basic Remindo model
    """

    def __init__(self, db_connector):
        self.db_connector = db_connector
        settings = db_connector.settings

    def get_lrs_object_id(self, activity):
        return get_object_id(activity)

    def get_info(self):
        return {
            "title": "H5P"
        }
