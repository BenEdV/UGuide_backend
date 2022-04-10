from copy import deepcopy
from datetime import timedelta
from isodate import parse_duration, duration_isoformat

import learnlytics.database.studydata as md
from learnlytics.extensions import db


def update_question_score(question_result):
    """
    Update the score of the questionresult
    :param question_result: The questionresult to update the score for
    :return:
    """
    given_answer = md.Answer.query.filter(md.Answer.id == question_result.given_answer_id).one_or_none()
    if given_answer:
        question_result.score = given_answer.score
    else:
        given_answers = question_result.given_answer_body.strip("{}").split(",")
        answers = md.Answer.query.filter(md.Answer.question_id == question_result.question_id).all()
        for answer in answers:
            if answer.remote_id[-1] in given_answers:
                question_result.score += answer.score


def update_question_max_score(question):
    """
    Update the max_score of the question
    :param question: The question to update the max score for
    :return:
    """
    scores = [answer.score for answer in question.answers]
    question.max_score = sum(scores)


def update_question_properties(activity_id):
    question = md.Activity.query.filter(md.Activity.id == activity_id).one()
    if not question.type.name.startswith("question"):
        return
    exams = question.tail_activities

    lrs_connector = question.collection.main_lrs_connector()
    # Get all results
    params = {
        "statement.object.id": question.lrs_object_id
    }
    response_per_user = {}
    amount_correct = 0
    amount_total = 0
    total_time = timedelta(seconds=0)

    for statement in lrs_connector.model.get_statements(params):
        if "result" not in statement:
            continue
        if "response" not in statement["result"]:
            continue
        if "account" in statement["actor"]:
            user_id = statement["actor"]["account"]["name"]
        else:
            user_id = statement["actor"]["mbox"]
        response_per_user[user_id] = statement["result"]["response"]
        amount_total += 1
        if statement["result"].get("success", False):
            amount_correct += 1
        if "duration" in statement["result"]:
            total_time += parse_duration(statement["result"]["duration"])

    for answer in question.properties.get("answers", []):
        if "avg_scores" not in answer:
            answer["avg_scores"] = {}

    for exam in exams:
        if not exam.type.name == "exam":
            continue
        params = {
            "statement.object.id": exam.lrs_object_id
        }
        grades_per_response = {}

        for statement in lrs_connector.model.get_statements(params):
            if "result" not in statement:
                continue
            if "account" in statement["actor"]:
                user_id = statement["actor"]["account"]["name"]
            else:
                user_id = statement["actor"]["mbox"]
            if "extensions" not in statement["result"]:
                continue
            for extension, value in statement["result"]["extensions"].items():
                if extension.split("/")[-1] == "grade":
                    if response_per_user[user_id] not in grades_per_response:
                        grades_per_response[response_per_user[user_id]] = []
                    grades_per_response[response_per_user[user_id]].append(value)
                break

        average_grade_per_response = {}
        for response, grades in grades_per_response.items():
            average_grade_per_response[response] = sum(grades) / len(grades)
        for answer in question.properties.get("answers", []):
            if answer["id"] not in average_grade_per_response:
                continue
            answer["avg_scores"][exam.id] = average_grade_per_response[answer["id"]]

    if "answers" in question.properties:
        question.properties["answers"] = deepcopy(question.properties["answers"])
    if amount_total > 0:
        question.properties["avg_score"] = amount_correct / amount_total
        question.properties["avg_duration"] = duration_isoformat(total_time / amount_total)
    db.session.commit()
