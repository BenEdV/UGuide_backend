
"""
Contains the RemindoRecipeModel, which handles all request related to recipes.
"""

from learnlytics.connectors.learninglocker.models import LearningLockerSubModel


class LearningLockerStoreModel(LearningLockerSubModel):

    def get_stores(self):
        return self.connector.get_store()

    def get_store(self, store_id):
        return self.connector.get_store(store_id=store_id)

    def create_store(self, title):
        json = {
            "title": title,
            "organisation": self.connector.organisation_id
        }
        return self.connector.post_store(json=json)
