from bs4 import BeautifulSoup
import requests
from flask_restplus import abort


from learnlytics.extensions import db
from learnlytics.database.authorization.collection import Collection
import learnlytics.database.studydata as md
from learnlytics.util.requests import get_filename_from_cd


class Exams(object):
    """
    The model for an exam to use
    """

    def __init__(self, forced=False):
        """
        :param forced: If forced = True, will call the force upsert instead of upsert
        This will delete the entry if it exists and re-add it.
        """
        self.forced = forced

    def add_activity(self, collection_id, data, source=""):
        if data.get("title", None) is None or data.get("title", None) == "":
            collection = Collection.get(collection_id)
            title = "Activity " + str(collection.activities.count() + 1)
        else:
            title = data["title"]

        activity_type = md.ActivityType.query.filter(md.ActivityType.name == data["type"]).one_or_none()
        if activity_type is None:
            activity_type = md.ActivityType.query.filter(md.ActivityType.name == data["type"]).one_or_none()

        activity = md.Activity(
            collection_id=collection_id,
            remote_id=str(data["remote_id"]),
            title=title,
            properties={},
            type_id=activity_type.id,
            visibility="T")

        db.session.add(activity)
        db.session.flush()
        self.update_activity(collection_id, activity, data, source=source)

        return activity.id

    def update_activity(self, collection_id, activity, data, source=""):
        print("Update activity")
        if "title" in data:
            activity.title = data["title"]
        if "body" in data:
            activity.properties["body"] = data["body"]
        if "answers" in data:
            activity.properties["answers"] = data["answers"]
        if "incomplete" in data:
            activity.properties["incomplete"] = data["incomplete"]

        if "parent_id" in data:
            parent_activity = md.Activity.query.filter(
                md.Activity.collection_id == collection_id,
                md.Activity.remote_id == data["parent_id"]).one()
            relation_type = md.ActivityRelationType.query.filter(
                md.ActivityRelationType.name == "exam_question").one_or_none()

            relation = md.ActivityRelation(
                tail_activity_id=parent_activity.id,
                head_activity_id=activity.id,
                type=relation_type,
                properties={
                    "number": data["number"]
                })
            print(f"relation number: {data['number']}")
            db.session.add(relation)
        db.session.add(activity)
        db.session.flush()

    def add_exam(self, collection_id, exam_data, source=""):  # pylint: disable=too-many-locals
        """
        Parses the Post body to add an exam to the database
        :param course: The course the exam should be added to
        :param source: The external source where this exam is loaded from
        :param exam_data: A json object with the structure
        {
          "remote_exam_id": str,
          "type": str,
          "title": str,
          "max_score": int,
          "questions": [
            {
              "remote_question_id": str,
              "type": str,
              "body": str,
              "max_score": int,
              "p_value": float,
              "std_value": float,
              "rit_value": float,
              "rir_value": float,
              "answers": [
                {
                  "remote_answer_id": str,
                  "body": str,
                  "correct": bool,
                  "score": float
                },
                {# more answers}
              ],
            },
            {# more questions}
          ]
        }
        :return: The exam object that was created
        """
        if exam_data["title"] is None or "":
            collection = Collection.get(collection_id)
            exam_title = "Exam " + str(collection.activities.count() + 1)
        else:
            exam_title = exam_data["title"]

        exam_type = md.ActivityType.query.filter(md.ActivityType.name == exam_data["type"]).one_or_none()
        if exam_type is None:
            exam_type = md.ActivityType.query.filter(md.ActivityType.name == "exam").one_or_none()

        exam = md.Activity(
            collection_id=collection_id,
            remote_id=source + "_" + str(exam_data["remote_exam_id"]),
            properties={"max_score": exam_data["max_score"]},
            title=exam_title,
            type_id=exam_type.id,
            visibility=exam_data.get("visibility", "F"))

        db.session.add(exam)
        db.session.flush()

        for question_index, question_dict in enumerate(exam_data["questions"]):
            question_id = question_dict["remote_question_id"]
            question_remote_id = source + "_" + question_id
            question_type = md.ActivityType.query.filter(
                md.ActivityType.name == question_dict["type"]).one_or_none()
            if question_type is None:
                abort(400, f"The type {question_dict['type']} is not supported")

            if "number" in question_dict and question_dict["number"] is not None:
                question_number = question_dict["number"]
            else:
                question_number = question_index + 1

            if "title" in question_dict and question_dict["title"] is not None:
                question_title = question_dict["title"]
            else:
                question_title = f"Question {question_number}"

            question = md.Activity(
                remote_id=question_remote_id,
                title=question_title,
                properties={
                    "body": question_dict.get("body", None),
                    "prompt": question_dict.get("prompt", None),
                    "max_score": question_dict["max_score"],
                    "answers": question_dict["answers"]},
                type_id=question_type.id,
                collection_id=collection_id,
                visibility="F")
            db.session.add(question)
            db.session.flush()

            from learnlytics.models.activities import ActivitiesModel
            for image_url in question_dict.get("image_urls", []):
                response = requests.get(image_url)

                filename = get_filename_from_cd(response.headers["Content-Disposition"].replace('"', ''))

                attachment = ActivitiesModel.add_attachment_from_content(question.id, response.content, filename)
                # Replace image_urls in question bodies and answers
                # questions
                question_properties = question.properties
                body = question_properties["body"]
                soup = BeautifulSoup(body, "html.parser")
                for img in soup.findAll("img"):
                    if img["src"] == image_url:
                        img["src"] = attachment.source_url
                question_properties["body"] = str(soup)
                # answers
                for answer in question_properties["answers"]:
                    body = answer["body"]
                    soup = BeautifulSoup(body, "html.parser")
                    for img in soup.findAll("img"):
                        if img["src"] == image_url:
                            img["src"] = attachment.source_url
                    answer["body"] = str(soup)

                question.properties = question_properties

            relation_type = md.ActivityRelationType.query.filter(
                md.ActivityRelationType.name == "exam_question").one_or_none()

            relation = md.ActivityRelation(
                tail_activity_id=exam.id,
                head_activity_id=question.id,
                type=relation_type,
                properties={
                    "number": question_number
                })
            db.session.add(relation)

        db.session.commit()
        return exam
