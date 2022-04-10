
"""
This module contains the local model
"""

from learnlytics.connectors.model import ConnectorModel

from learnlytics.connectors.local.utils import get_object_id


class LocalModel(ConnectorModel):  # pylint: disable=too-few-public-methods
    """
    Basic Local model
    """

    def __init__(self, db_connector):
        self.db_connector = db_connector
        settings = db_connector.settings

    def get_lrs_object_id(self, activity):
        return get_object_id(activity)

    def get_info(self):
        return {
            "title": "Local"
        }
