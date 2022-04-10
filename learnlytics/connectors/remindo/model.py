
"""
This module contains the Remindo model
"""
import logging

from learnlytics.connectors.model import ConnectorModel
from learnlytics.connectors.remindo.connector import RemindoConnector

from learnlytics.connectors.remindo.models.result_model import RemindoResultModel
from learnlytics.connectors.remindo.utils import get_lrs_actor, get_object_id

logger = logging.getLogger("remindo")


class RemindoModel(ConnectorModel):  # pylint: disable=too-few-public-methods
    """
    Basic Remindo model
    """

    def __init__(self, db_connector):
        self.db_connector = db_connector
        settings = db_connector.settings
        base_url = settings["base_url"]
        uuid = settings["uuid"]
        secret = settings["secret"]
        logger.debug(f"Init remindo model with :{base_url}, {uuid}, {secret}")
        self.connector = RemindoConnector(base_url, uuid, secret)

        from learnlytics.connectors.remindo.models.exam_model import RemindoRecipeModel
        from learnlytics.connectors.remindo.models.moment_model import RemindoMomentModel
        from learnlytics.connectors.remindo.models.person_model import RemindoUserModel
        from learnlytics.connectors.remindo.models.callback_model import RemindoCallbackModel
        self.exam_model = RemindoRecipeModel(self.connector, db_connector.code, settings)
        self.result_model = RemindoResultModel(self.connector, db_connector.code, settings)
        self.moment_model = RemindoMomentModel(self.connector, db_connector.code, settings)
        self.person_model = RemindoUserModel(self.connector, db_connector.code, settings)
        self.callback_model = RemindoCallbackModel(self.connector, db_connector.code, settings)

    def get_info(self):
        info = {
            "title": self.db_connector.title,
            "code": self.db_connector.code,
            "settings": self.db_connector.settings
        }

        return info

    def get_exams_minimal(self):
        return self.exam_model.get_exams_minimal()

    def add_exam_to_collection(self, collection_id, recipe_id, data):
        return self.exam_model.add_exam_to_collection(collection_id, recipe_id, data)

    def get_results(self, exam):
        return self.result_model.get_results(exam)

    def get_recipe_moments(self, recipe_id):
        return self.moment_model.get_moments_for_recipe(recipe_id)

    def get_moment_candidates(self, moment_id):
        return self.moment_model.get_moment_candidates(moment_id, full=True)

    def load_candidates(self, exam):
        return self.person_model.get_candidates(exam)

    def test(self, data):
        return self.connector._query(data["url"], data["params"])

    def get_lrs_actor(self, person):
        return get_lrs_actor(self.connector.base_url, person.remote_id.split("_")[-1])

    def get_lrs_object_id(self, activity):
        return get_object_id(self.connector.base_url, activity)

    def callback(self, request):
        return self.callback_model.handle_callback(request)
