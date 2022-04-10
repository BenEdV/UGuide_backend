import logging

from learnlytics.api.models.result_model import Result as ApiResultModel
from learnlytics.connectors.remindo.models import RemindoSubModel
from learnlytics.connectors.remindo.models.result_model import RemindoResultModel
import learnlytics.connectors.remindo.utils as utils
import learnlytics.database.studydata as md

logger = logging.getLogger("remindo")


class RemindoCallbackModel(RemindoSubModel):

    def handle_callback(self, request):
        data = request.json

        # if not utils.verify_signature(
        #         data,
        #         str(self.connector.secret),
        #         self.connector.base_url,
        #         data['signature']):
        #     raise Exception("Remindo signature does not match payload")
        payload = utils.json.loads(data['payload'])
        logger.debug(f"Received callback with payload\n{utils.json.dumps(payload, indent=4, sort_keys=True)}")
        user_id = payload["data"]["user_id"]

        if payload["action"] == "subscription_finish":
            logger.info(f"User with Remindo id {user_id} finished exam")
        elif payload["action"] == "result_change_grade":
            logger.info(f"User with Remindo id {user_id} changed their grade")
            self.handle_subscription_finish(payload["data"])
        elif payload["action"] == "subscription_start":
            logger.info(f"User with Remindo id {user_id} started exam")
        elif payload["action"] == "subscription_create":
            logger.info(f"User with Remindo id {user_id} created exam")
        else:
            print(payload["action"])

    def handle_subscription_finish(self, data):
        recipe_id = data["recipe_id"]
        moment_id = data["moment_id"]
        remote_id = f"{self.code}_{recipe_id}"

        exam_type = md.ActivityType.query.filter(md.ActivityType.name == "exam").one()
        exams = md.Activity.query.filter(md.Activity.type_id == exam_type.id, md.Activity.remote_id == remote_id).all()

        rem_user_id = data["user_id"]
        person_id = f"{self.code}_{rem_user_id}"
        person = md.Person.query.filter(md.Person.remote_id == person_id).one_or_none()

        result_model = RemindoResultModel(self.connector, self.code, self.settings)
        for exam in exams:
            if moment_id not in exam.properties["remindo"]["moments"]:
                logger.warning(f"{exam.id} does not have moment {moment_id}")
                continue
            if exam.properties["remindo"]["import_exam_result_on_completion"]:
                if exam.properties["remindo"]["import_question_result_on_completion"]:
                    logger.info(f"Adding exam and question results for user with Remindo id {rem_user_id}")
                    result_model.get_results(exam, [rem_user_id])
                else:
                    logger.info(f"Adding exam result for user with Remindo id {rem_user_id}")
                    statement = result_model.exam_statement_for_result(data)
                    data = [(exam.id, person.user_id, statement)]
                    ApiResultModel.add_results(data, exam.collection_id)
