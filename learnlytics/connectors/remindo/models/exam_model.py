
"""
Contains the RemindoRecipeModel, which handles all request related to recipes.
"""

from bs4 import BeautifulSoup

from learnlytics.api.models.exams import Exams as ExamModel
from learnlytics.connectors.remindo.models import RemindoSubModel
from learnlytics.connectors.remindo.models.moment_model import RemindoMomentModel
from learnlytics.database.authorization.collection import Collection
from learnlytics.extensions import db
from learnlytics.models.activities import ActivitiesModel


class RemindoRecipeModel(RemindoSubModel):
    """
    Handle all requests related to recipes
    Notes:
    !!! The answer "titles" in the html of the item do not always agree with the "indentifiers" in
    !!! qtidata.RESPONSE.interaction.simpleChoice and therefore also do not agree with the identifiers in
    !!! qtidata.RESPONSE.scoring.correctResponse.values
    """
    exam_model = ExamModel()

    def get_exams_minimal(self):
        return self.get_recipes()

    def add_exam_to_collection(self, collection_id, recipe_id, data):
        """
        Creates an exam with the data retrieved from remindo for the given recipe_id and attaches it to the given course
        """
        recipe_data = self.get_recipes(recipe_id=recipe_id, full=True)

        if "title" in data:
            recipe_data["title"] = data["title"]
        if "visibility" in data:
            recipe_data["visibility"] = data['visibility']
        if "moments" in data:
            moment_id = data["moments"][0]

        collection = Collection.get(collection_id, required=True)
        new_exam = self.exam_model.add_exam(collection_id, recipe_data, self.code)
        new_exam.properties["remindo"] = data["properties"] if "properties" in data else {}

        new_exam.properties["remindo"]["moments"] = [moment_id]

        activity_ids = [new_exam.id]
        for question in new_exam.head_activities:
            activity_ids.append(question.id)

        db.session.commit()

        mom_model = RemindoMomentModel(self.connector, self.code, self.settings)
        mom_model.attach_moment_to_exam(new_exam, moment_id)

        return ActivitiesModel.get_activities(activity_ids)

    def get_recipes(self, recipe_id=None, study_id=None, full=False):
        """
        Returns the recipes. The full format will include max score and questions.
        :param recipe_id: (int, optional, default None) id of the recipe.
        :param study_id: (int, optional, default None) id of the study.
        :param full: (bool, optional, default False) return full information.
        :return: The requested recipe(s).
        """

        params = {}
        if recipe_id:
            params["recipe_id"] = recipe_id
        if study_id:
            params["study_id"] = study_id

        data = self.connector.recipe_list(params)
        recipes = []

        for recipe in data["recipes"].values():
            recipe_info = {
                "remote_exam_id": recipe["id"],
                "type": recipe["type"],
                "title": recipe["name"],
                "study_id": recipe["study_id"]}

            if full:
                max_score = 0
                recipe_items = self.get_recipe_items(recipe["id"])
                for item in recipe_items:
                    max_score += item["max_score"]
                recipe_info["max_score"] = max_score
                recipe_info["questions"] = recipe_items

            if recipe_id:
                return recipe_info

            recipes.append(recipe_info)

        return recipes

    def get_recipe_items(self, recipe_id):
        """
        Returns all items (questions + answers) of a recipe.
        :param recipe_id: The recipe_id to return the items for.
        :return: A list containing dictionaries containing questions with answers
        """
        params = {"recipe_id": recipe_id}
        if "tutor_id" in self.settings:
            params["tutor_id"] = self.settings["tutor_id"]
        else:
            params["tutor_filter"] = "*"
        item_view_data = self.connector.item_view(params)

        items = item_view_data.get("items")
        questions = []
        for item in items:
            question_body, image_urls = self.parse_html_to_question(item["html"])

            question_prompt = self.parse_html_to_question_prompt(item["html"])

            answers = self.get_answers(item["metadata"]["qtidata"]["RESPONSE"], item["html"])
            if answers is None:
                answers = []

            for answer in answers:
                answer["remote_answer_id"] = f"{item.get('item_identifier')}_{answer['id']}"

            answers.sort(key=lambda x: x["remote_answer_id"])

            title = item.get("metadata").get("code")
            if title == "":
                title = None

            questions.append({
                "remote_question_id": item.get("item_identifier"),
                "number": item.get("sequence_index"),
                "title": title,
                "type": self.get_question_type(item),
                "body": question_body,
                "prompt": question_prompt,
                "max_score": item.get("metadata").get("max_score"),
                "answers": answers,
                "image_urls": image_urls})
        return questions

    @staticmethod
    def get_question_type(item):
        metadata = item.get("metadata")
        if metadata["type"] == "choice":
            if item["result"]["response"]["RESPONSE"]["cardinality"] == "single":
                return "question.multiple_choice"
            if item["result"]["response"]["RESPONSE"]["cardinality"] == "multiple":
                return "question.multiple_selection"
        if metadata["type"] == "extended_text":
            return "question.open"
        if metadata["type"] == "text_entry":
            return "question.open"

    def get_answers(self, response, html):
        result = []
        interaction = response["interaction"]

        correct_answers = response["scoring"]["correctResponse"]["values"]

        if "simpleChoice" not in interaction:
            return None

        for answer in response["interaction"]["simpleChoice"]:
            identifier = answer["identifier"]

            result.append({
                "id": identifier,
                "body": answer["flowStaticHTML"],
                "correct": identifier in correct_answers
            })

        return result

    @staticmethod
    def parse_html_to_question_prompt(html):
        """
        Strip html from Remindo payload and return question body
        :param html:
        :return: "Is this a sample question?"
        """
        source_code = html.replace("\\", "")
        soup = BeautifulSoup(source_code, "html.parser")
        question = soup.findAll("div", {"class": "qti-prompt"})
        if len(question) > 0:
            return str(question[0])
        return None

    @staticmethod
    def parse_html_to_question(html):
        """
        Strip html from Remindo payload and return question body
        :param html:
        :return: "Is this a sample question?"
        """
        image_urls = []
        source_code = html.replace("\\", "")
        soup = BeautifulSoup(source_code, "html.parser")
        for img in soup.findAll("img"):
            image_urls.append(img.get("src"))
        for div in soup.findAll("div", {"class": "qti-interaction"}):
            div.decompose()
        soup.div.unwrap()

        return str(soup), image_urls

    @staticmethod
    def parse_html_to_answers(html):
        """
        Strip html from remindo payload and return all posible answers for a given html string
        :param html:
        :return:
        [
            {
                "answer_id": int
                "body": str
                "correct": bool
            },
            {
                "answer_id": int
                "body": str
                "correct": bool
            }
        ]
        """
        source_code = html.replace("\\", "")
        soup = BeautifulSoup(source_code, "html.parser")
        answers_html = soup.findAll("div", {"class": "qti-simpleChoice"})
        inputs_html = soup.findAll("input")
        if len(inputs_html) > 0:
            answers = []
            i = 0
            for answer_html in answers_html:
                answer = {
                    "id": inputs_html[i]['title'],
                    "body": str(answer_html)
                }
                answers.append(answer)
                i += 1
            return answers
        return None
