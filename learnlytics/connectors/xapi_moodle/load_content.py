# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course (3 4)
# (C) Copyright Utrecht University (Department of Information and Computing Sciences)

from learnlytics.authorization.manager import authorize
from learnlytics.api.models.exams import Exams as ExamModel
from learnlytics.analyse.exam import average_duration, average_grade
from learnlytics.analyse.question import update_question_properties
import learnlytics.database.studydata as md
from learnlytics.extensions import db
from learnlytics.util.datetime import strptime_frontend

supported_hvp_categories = [
    {
        "id": "http://h5p.org/libraries/H5P.QuestionSet-1.17",
        "objectType": "Activity"
    },
    {
        "id": "http://h5p.org/libraries/H5P.InteractiveVideo-1.22",
        "objectType": "Activity"
    },
    {
        "id": "http://h5p.org/libraries/H5P.Summary-1.10",
        "objectType": "Activity"
    },
    {
        "id": "http://h5p.org/libraries/H5P.Blanks-1.12",
        "objectType": "Activity"
    },
    {
        "id": "http://h5p.org/libraries/H5P.MultiChoice-1.14",
        "objectType": "Activity"
    }
]


def new_statement(statement, collection_id):
    print("New statement")
    if "category" not in statement["context"]["contextActivities"].keys():
        return
    if statement["context"]["contextActivities"]["category"][0] not in supported_hvp_categories:
        return
    if statement["verb"]["id"] != "http://adlnet.gov/expapi/verbs/completed" and\
            statement["verb"]["id"] != "http://adlnet.gov/expapi/verbs/answered":
        return

    exisiting_activity = md.Activity.query.filter(
        md.Activity.collection_id == collection_id,
        md.Activity.remote_id == statement["object"]["id"]
    ).one_or_none()

    activity_id = None
    parent_activity_id = None

    print(exisiting_activity)
    if exisiting_activity is None:
        activity = transform_activity(statement)

        if "parent" in statement["context"]["contextActivities"].keys():
            parent_id = statement["context"]["contextActivities"]["parent"][0]["id"]
            activity["parent_id"] = parent_id
            exisiting_parent_activity = md.Activity.query.filter(
                md.Activity.collection_id == collection_id,
                md.Activity.remote_id == parent_id
            ).one_or_none()
            if exisiting_parent_activity is None:
                parent_activity = {
                    "remote_id": parent_id,
                    "type": "exam",
                    "incomplete": True
                }

                print("new parent")
                parent_activity_id = ExamModel().add_activity(collection_id, parent_activity, "hvp")

        print("new activity")
        activity_id = ExamModel().add_activity(collection_id, activity, "hvp")
    elif exisiting_activity.properties.get("incomplete", False):
        activity = transform_activity(statement)
        activity["incomplete"] = False
        activity_id = ExamModel().update_activity(collection_id, exisiting_activity, activity, "hvp")

    if activity_id:
        # update scores
        average_grade(activity_id)
        average_duration(activity_id)
        update_question_properties(activity_id)

    if parent_activity_id:
        # update scores
        average_grade(parent_activity_id)
        average_duration(parent_activity_id)
        update_question_properties(parent_activity_id)

    db.session.commit()


def load_results(collection, since_date=None):
    """
    :param lrs_id: The lrs which should be scanned for new results
    """
    lrs_connector = collection.main_lrs_connector()

    exisiting_id_tuples = db.session.query(md.Activity.remote_id).\
        filter(md.Activity.collection_id == collection.id).all()
    exisiting_ids = [e_id.split("_")[1] for e_id, in exisiting_id_tuples]
    if authorize(collection, ["manage_activities"], do_abort=False):
        # Get all statements for supported types

        params = {
            "statement.context.contextActivities.category": {"$in": supported_hvp_categories},
            "statement.verb.id": "http://adlnet.gov/expapi/verbs/completed"
        }
        if since_date:
            params["stored"] = {"$gt": strptime_frontend(since_time)}

        activities = {}
        for statement in lrs_connector.model.get_statements(params):
            object_id = statement["object"]["id"]

            if object_id not in exisiting_ids:
                activity = transform_activity(statement)

                activities[object_id] = activity
                exisiting_ids.append(object_id)

        # Add exams to database
        for exam in exams.values():
            ExamModel().add_exam(collection.id, exam, "hvp")


def transform_activity(statement):
    object_type = statement["context"]["contextActivities"]["category"][0]["id"]
    if object_type == "http://h5p.org/libraries/H5P.QuestionSet-1.17":
        return transform_exam(statement)
    if object_type == "http://h5p.org/libraries/H5P.Blanks-1.12":
        return transform_open_question(statement)
    if object_type == "http://h5p.org/libraries/H5P.MultiChoice-1.14":
        return transform_multiple_choice_question(statement)
    if object_type == "http://h5p.org/libraries/H5P.InteractiveVideo-1.22":
        return transform_video(statement)
    if object_type == "http://h5p.org/libraries/H5P.Summary-1.10":
        return transform_summary(statement)

    return None


def transform_exam(statement):
    object_id = statement["object"]["id"]
    exam = {
        "title": list(statement["object"]["definition"]["name"].values())[0],
        "remote_id": object_id,
        "type": "exam",
        "max_score": statement["result"]["score"]["max"],
        "questions": []
    }

    return exam


def transform_multiple_choice_question(statement):
    object_id = statement["object"]["id"]
    correct_answers = statement["object"]["definition"]["correctResponsesPattern"]
    answers = []
    for answer in statement["object"]["definition"]["choices"]:
        answers.append({
            "id": answer["id"],
            "body": list(answer["description"].values())[0],
            "correct": answer["id"] in correct_answers
        })

    description = statement["object"]["definition"].get("description", {})
    if description == {}:
        description = None
    else:
        description = list(description.values())[0]

    question = {
        "title": list(statement["object"]["definition"]["name"].values())[0],
        "body": description,
        "answers": answers,
        "number": statement["context"]["extensions"]["http://id.tincanapi.com/extension/ending-point"],
        "remote_id": object_id,
        "max_score": statement["result"]["score"]["max"],
        "type": "question.multiple_choice"
    }

    return question


def transform_open_question(statement):
    object_id = statement["object"]["id"]
    correct_answers = statement["object"]["definition"]["correctResponsesPattern"]

    question = {
        "title": statement["object"]["definition"]["name"]["en-US"],
        "body": statement["object"]["definition"].get("description", {}).get("en-US", None),
        "correct_answers": correct_answers,
        "number": statement["context"]["extensions"]["http://id.tincanapi.com/extension/ending-point"],
        "answers": [],
        "remote_id": object_id,
        "max_score": statement["result"]["score"]["max"],
        "type": "question.open"
    }

    return question


def transform_video(statement):
    object_id = statement["object"]["id"]

    video = {
        "title": statement["object"]["definition"]["name"]["en-US"],
        "body": statement["object"]["definition"].get("description", {}).get("en-US", None),
        "answers": [],
        "remote_id": object_id,
        "max_score": statement["result"]["score"]["max"],
        "type": "question.open"
    }

    return video


def transform_summary(statement):
    object_id = statement["object"]["id"]
    correct_answers = statement["object"]["definition"]["correctResponsesPattern"]

    summary = {
        "title": statement["object"]["definition"]["name"]["en-US"],
        "body": statement["object"]["definition"].get("description", {}).get("en-US", None),
        "correct_answers": correct_answers,
        "answers": [],
        "remote_id": object_id,
        "max_score": statement["result"]["score"]["max"],
        "type": "question.open"
    }

    return summary
