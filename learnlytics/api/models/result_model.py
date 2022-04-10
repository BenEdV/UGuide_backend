from flask_restplus import abort

from learnlytics.extensions import db
import learnlytics.database.studydata as md
from learnlytics.database.authorization.collection import Collection


class Result(object):
    """
    Model to add a result
    """

    @staticmethod
    def add_results(data, collection_id):
        """
        :param data: Array of tuples containing (activity_id, user_id, statement)
        """
        activity_ids = []
        user_ids = []
        statements = []

        for (activity_id, user_id, statement) in data:
            print(activity_id, user_id, statement)
            activity_ids.append(activity_id)
            user_ids.append(user_id)
            statements.append(statement)

        collection = Collection.get(collection_id, required=True)
        lrs_connector = collection.main_lrs_connector()
        result = lrs_connector.model.post_statements(statements)

        Result.calculate_construct_scores(collection, data, activity_ids, user_ids)

        return result

    @staticmethod
    def calculate_construct_scores(collection, data, activity_ids, user_ids):
        for model in collection.construct_models:
            model.implementation_model.add_new_results(data, activity_ids, user_ids)
