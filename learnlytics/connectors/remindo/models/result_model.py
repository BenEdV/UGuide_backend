
"""
This module contains the Remindo result model
"""
import datetime
from isodate import duration_isoformat
import uuid

from learnlytics.api.models.result_model import Result as ApiResultModel
from learnlytics.connectors.remindo.models import RemindoSubModel
from learnlytics.connectors.remindo.utils import time_from_string, get_recipe_id, get_moment_id, get_lrs_actor
import learnlytics.database.studydata as md


class RemindoResultModel(RemindoSubModel):
    """
    The model for a Remindo result and functions on results
    """

    # The max amount of item results that a Remindo call will return
    max_items = 50_000
    user_id_for_subscription = {}
    question_count_for_user_id = {}
    timestamp_for_subscription = {}
    user_id_for_person_id = {}
    activity_id_for_item_id = {}

    def get_results(self, exam, user_ids=None):
        """
        Gets the results of a given exam for each of the given users.
        :param exam: Activity object with remote_id in Remindo
        :param user_ids: The remote ids of the users
        """
        recipe_id = get_recipe_id(exam)
        moment_id = get_moment_id(exam)

        if user_ids is None:
            persons = md.Person.query.all()
        else:
            person_ids = []
            for remote_user_id in user_ids:
                person_ids.append(f"{self.code}_{remote_user_id}")
            persons = md.Person.query.filter(md.Person.remote_id.in_(person_ids)).all()
        for person in persons:
            self.user_id_for_person_id[int(person.remote_id.split("_")[-1])] = person.user_id

        self.activity_id_for_item_id[recipe_id] = exam.id
        for question in exam.head_activities:
            self.activity_id_for_item_id[question.remote_id.split("_")[-1]] = question.id

        result_tuples = self.get_exam_results(recipe_id, moment_id, user_ids)

        if result_tuples == []:
            return

        user_id_sets = self.create_user_sets()

        for user_id_set in user_id_sets:
            result_tuples.extend(self.get_item_results(recipe_id, moment_id, user_id_set))

        ApiResultModel.add_results(result_tuples, exam.collection_id)

    def get_exam_results(self, recipe_id, moment_id, user_ids):
        """
        Get results from Remindo and add them to a paginated dictionary
        :param params: The paramaters to the Remindo query
        :return: A list of dictionaries with results
        """
        if moment_id is None:
            exam_types = ["exam", "practice", "graded practice"]

            params = {
                "recipe_ids": [recipe_id],
                "types": exam_types,
            }

            if user_ids is not None:
                params["user_ids"] = user_ids

            results = self.get_results_helper(params)
        else:
            results = self.get_moment_results(moment_id, user_ids)

        # Strip away information from Remindo that we do not use
        result_tuples = []

        for result in results:
            exam_statement = self.exam_statement_for_result(result)
            self.user_id_for_subscription[result["subscription_id"]] = result["user_id"]
            self.timestamp_for_subscription[result["subscription_id"]] = time_from_string(result["end_time"]).\
                isoformat()
            self.question_count_for_user_id[result["user_id"]] = result["i_count"]

            result_tuples.append((
                self.activity_id_for_item_id[recipe_id],
                self.user_id_for_person_id.get(result["user_id"], None),
                exam_statement))

        return result_tuples

    def exam_statement_for_result(self, result):
        duration = time_from_string(result["end_time"]) - time_from_string(result["start_time"])

        statement_id = uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"{self.connector.base_url}/recipe_results/{result['result_id']}")

        exam_statement = {
            "id": str(statement_id),
            "actor": {
                "account": get_lrs_actor(self.connector.base_url, result["user_id"]),
                "objectType": "Agent"
            },
            "verb": {
                "id": "http://adlnet.gov/expapi/verbs/completed"
            },
            "object": {
                "id": f"{self.connector.base_url}/exams/{result['recipe_id']}",
                "objectType": "Activity"
            },
            "result": {
                "success": result["passed"],
                "score": {
                    "raw": result["score"],
                    "max": result["max_score"],
                    "min": 0
                },
                "extensions": {
                    f"{self.connector.base_url}/grade": result["grade"]
                },
                "duration": duration_isoformat(duration)
            },
            "timestamp": time_from_string(result["end_time"]).isoformat()
        }

        return exam_statement

    def get_moment_results(self, moment_id, user_ids):
        """
        Returns the results of a moment
        :param moment_id: The id of the moment
        :return: All results of the moment
        """
        params = {}
        params["id"] = moment_id
        if user_ids is not None:
            params["candidate_ids"] = user_ids

        data = self.connector.moment_results(params)
        return data["results"]

    def get_results_helper(self, params):
        """
        Helper for getting results; code utilized multiple times in one request
        :param params: params for Remindo request
        :return: results
        """
        results = []
        params["page_size"] = 200
        remindo_payload = self.connector.result_list(params)
        if remindo_payload:
            total_pages = remindo_payload["response"]["total_pages"]
            results.extend(remindo_payload["response"]["results"])
            for page in range(2, total_pages + 1):
                params["page"] = page
                results.extend(self.connector.result_list(params)["response"]["results"])
        return results

    def create_user_sets(self):
        """
        The item results has a limited number of results it can return. This will create sets of user_ids such that no
        set will return more than max_items item results.
        """
        user_id_sets = []
        current_user_set = []
        item_count = 0

        for user_id, question_count in self.question_count_for_user_id.items():
            if item_count + question_count > self.max_items:
                user_id_sets.append(current_user_set)
                current_user_set = []
            current_user_set.append(user_id)
            item_count += question_count

        user_id_sets.append(current_user_set)

        return user_id_sets

    def get_item_results(self, recipe_id, moment_id, user_ids):
        """
        Get item_results; the answer to a question.
        :param params: The parameters to the Remindo query.
        :return: A list of dictionaries containing results.
        """

        params = {
            "recipe_id": recipe_id,
            "user_ids": user_ids
        }

        if moment_id is not None:
            params["moment_id"] = moment_id

        remindo_payload = self.connector.itemresult_list(params)["itemresults"]

        result_tuples = []

        for subscription_id, value in remindo_payload.items():
            if int(subscription_id) not in self.user_id_for_subscription:
                print(subscription_id)
                continue
            for item_result in value:
                for result_id, item in item_result["itemresults"].items():
                    candidate_response = None
                    if "RESPONSE" in item["response"]:
                        candidate_response = item["response"]["RESPONSE"]["candidateResponse"]
                        if type(candidate_response) is list:
                            candidate_response = str.join(',', candidate_response)

                    if candidate_response is None:
                        candidate_response = ""

                    statement_id = uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        f"{self.connector.base_url}/sub/{subscription_id}/results/{result_id}")

                    duration = datetime.timedelta(seconds=item["duration"])
                    print(duration_isoformat(duration))
                    statement = {
                        "id": str(statement_id),
                        "actor": {
                            "account": get_lrs_actor(
                                self.connector.base_url,
                                self.user_id_for_subscription[int(subscription_id)]
                            ),
                            "objectType": "Agent"
                        },
                        "verb": {
                            "id": "http://adlnet.gov/expapi/verbs/answered"
                        },
                        "object": {
                            "id": f"{self.connector.base_url}/items/{item['item_identifier']}",
                            "objectType": "Activity"
                        },
                        "result": {
                            "success": item["passed"],
                            "score": {
                                "raw": item["score"],
                                "max": item["max_score"],
                                "min": 0
                            },
                            "response": candidate_response,
                            "extensions": {
                                f"{self.connector.base_url}/num_attempts": item["num_attempts"]
                            },
                            "duration": duration_isoformat(duration)
                        },
                        "timestamp": self.timestamp_for_subscription[int(subscription_id)]
                    }

                    result_tuples.append((
                        self.activity_id_for_item_id[item["item_identifier"]],
                        self.user_id_for_person_id.get(self.user_id_for_subscription[int(subscription_id)], None),
                        statement))

        return result_tuples
