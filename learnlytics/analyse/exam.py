from datetime import timedelta
import math
import numpy
from flask_restplus import abort
from sqlalchemy.sql.expression import literal
from itertools import combinations
from isodate import parse_duration, duration_isoformat

import learnlytics.database.studydata as md
from learnlytics.extensions import db
import learnlytics.analyse.question_value as aq


def update_exam_max_score(exam):
    """
    Update the exam max score
    :param exam: The exam to update the max score for
    :return:
    """
    questions = md.Question.query.filter(md.Question.exam == exam).all()
    max_scores = [question.max_score for question in questions]
    exam.max_score = numpy.sum(max_scores)


def update_exam_values(exam_id):
    """
    Update the exam max score
    :param exam_id: The ID of the exam to update the max score for
    :return:
    """
    questions = md.Question.query.filter(md.Question.exam_id == exam_id).all()
    for question in questions:
        aq.update_p_value(question)
        aq.update_std_value(question)
        aq.update_rir_value(question)
        aq.update_rit_value(question)


def update_exam_score(exam_result):
    """
    Updates the exam score
    :param exam_result: The examresult to update the score for
    :return:
    """
    question_results = md.QuestionResult.query.filter(md.QuestionResult.exam_result == exam_result).all()
    scores = [question.score for question in question_results]
    score_sum = numpy.sum(scores)
    exam_result.score = int(score_sum)
    exam = md.Exam.query.filter(md.Exam.id == exam_result.exam_id).one_or_none()
    exam_result.grade = float(score_sum) / exam.max_score * 10


def calculate_inter_item_correlation(collection, activity_ids):
    """
    Calculates the inter-item correlation between each pair of activities. This is the likelihood that a
    student gives either the right answer or wrong answer for both activities.
    """
    if db.session.query(literal(True)).filter(
            md.Activity.collection_id != collection.id, md.Activity.id.in_(activity_ids)).first():
        abort(409, f"Activities given do not all belong to collection {collection.name}")

    activity_results, user_ids = __get_statements_for_actvities(collection, activity_ids)

    correlation = {}

    for activity_a in activity_ids:
        correlation[activity_a] = {}
        for activity_b in activity_ids:
            correlation[activity_a][activity_b] = 0
            for user_id in user_ids:
                a_success = activity_results[activity_a][user_id]["result"]["success"]
                b_success = activity_results[activity_b][user_id]["result"]["success"]
                if a_success == b_success:
                    correlation[activity_a][activity_b] += 1 / len(user_ids)

    # clean up
    for activity_a in activity_ids:
        correlation[activity_a] = list(correlation[activity_a].values())

    return correlation


def calculate_rir_value(collection, activity_ids):
    if db.session.query(literal(True)).filter(
            md.Activity.collection_id != collection.id, md.Activity.id.in_(activity_ids)).first():
        abort(409, f"Activities given do not all belong to collection {collection.name}")
    if len(activity_ids) < 2:
        return {}
        # abort(400, f"There must be at least 2 activities to calculate rir values")
    rir_values = {}

    activity_results, user_ids = __get_statements_for_actvities(collection, activity_ids)

    total_score = {}
    for user_id in user_ids:
        total_score[user_id] = 0

    for activity_id in activity_ids:
        for user_id in user_ids:
            total_score[user_id] += activity_results[activity_id][user_id]["result"]["score"]["raw"]

    for activity_id in activity_ids:
        correct_scores = []
        incorrect_scores = []
        for user_id in user_ids:
            result = activity_results[activity_id][user_id]["result"]
            user_adjusted_score = total_score[user_id] - result["score"]["raw"]
            if "success" not in result:
                if result["score"]["max"] == result["score"]["raw"]:
                    correct_scores.append(user_adjusted_score)
                else:
                    incorrect_scores.append(user_adjusted_score)
            elif result["success"]:
                correct_scores.append(user_adjusted_score)
            else:
                incorrect_scores.append(user_adjusted_score)

        correct_scores = [x / (len(activity_ids) - 1) for x in correct_scores]
        incorrect_scores = [x / (len(activity_ids) - 1) for x in incorrect_scores]

        m_cor = numpy.mean(correct_scores)
        m_inc = numpy.mean(incorrect_scores)
        total_correct = float(len(correct_scores))
        total_incorrect = float(len(incorrect_scores))

        scores = incorrect_scores + correct_scores
        std = numpy.std(scores, ddof=1)
        total = total_correct + total_incorrect

        rir_value = None
        if total > 0:
            rir_value = (m_cor - m_inc) / std * math.sqrt((total_correct * total_incorrect) / (total * total))

            if numpy.isnan(rir_value):
                rir_value = None

        rir_values[activity_id] = rir_value

    return rir_values


def average_grade(activity_id):
    # results
    activity = md.Activity.query.filter(md.Activity.id == activity_id).one()
    if not activity.type.name.startswith("exam"):
        return
    lrs_connector = activity.collection.main_lrs_connector()
    # Get all results
    params = {
        "statement.object.id": activity.lrs_object_id
    }
    all_grades = []

    for statement in lrs_connector.model.get_statements(params):
        if "result" not in statement:
            continue
        if "extensions" not in statement["result"]:
            continue
        for extension, value in statement["result"]["extensions"].items():
            if extension.split("/")[-1] == "grade":
                all_grades.append(value)
                break

    # Calculate average grade
    if len(all_grades) > 0:
        activity.properties["average"] = sum(all_grades) / len(all_grades)
    if len(all_grades) > 2:
        std_dev = numpy.std(all_grades, ddof=1)
        if numpy.isnan(std_dev):
            std_dev = None
        activity.properties["std_dev"] = std_dev

    db.session.commit()


def average_duration(activity_id):
    # results
    activity = md.Activity.query.filter(md.Activity.id == activity_id).one()
    if not activity.type.name.startswith("exam"):
        return
    lrs_connector = activity.collection.main_lrs_connector()
    # Get all results
    params = {
        "statement.object.id": activity.lrs_object_id
    }
    all_durations = []
    passed_durations = []

    for statement in lrs_connector.model.get_statements(params):
        if "result" not in statement:
            continue
        if "duration" not in statement["result"]:
            continue
        duration = parse_duration(statement["result"]["duration"]).seconds
        all_durations.append(duration)
        if "success" not in statement["result"]:
            if statement["result"]["score"]["max"] == statement["result"]["score"]["raw"]:
                passed_durations.append(duration)
        elif statement["result"]["success"]:
            passed_durations.append(duration)

    # Calculate average duration for all
    if len(all_durations) > 0:
        avg_in_seconds = sum(all_durations) / len(all_durations)
        activity.properties["avg_duration"] = duration_isoformat(timedelta(seconds=avg_in_seconds))
    if len(all_durations) > 2:
        std_dev = numpy.std(all_durations, ddof=1)
        if numpy.isnan(std_dev):
            std_dev = None
        activity.properties["std_dev_duration"] = duration_isoformat(timedelta(seconds=std_dev))

    # Calculate average duration for passed exams
    if len(passed_durations) > 0:
        avg_in_seconds = sum(passed_durations) / len(passed_durations)
        activity.properties["avg_duration_passed"] = duration_isoformat(timedelta(seconds=avg_in_seconds))
    if len(passed_durations) > 2:
        std_dev = numpy.std(passed_durations, ddof=1)
        if numpy.isnan(std_dev):
            std_dev = None
        activity.properties["std_dev_duration_passed"] = duration_isoformat(timedelta(seconds=std_dev))

    db.session.commit()


def __get_statements_for_actvities(collection, activity_ids):
    activities = md.Activity.query.filter(md.Activity.id.in_(activity_ids)).all()
    activity_id_for_remote = {}
    object_ids = []
    for activity in activities:
        if activity.lrs_object_id is not None:
            activity_id_for_remote[activity.lrs_object_id] = activity.id
            object_ids.append(activity.lrs_object_id)

    lrs_connector = collection.main_lrs_connector()

    user_ids = set()
    activity_results = {}
    for activity_id in activity_ids:
        activity_results[activity_id] = {}

    params = {
        "statement.object.id": {"$in": object_ids}
    }

    for statement in lrs_connector.model.get_statements(params):
        if "result" not in statement or "score" not in statement["result"]:
            continue
        object_id = statement["object"]["id"]
        if "account" in statement["actor"]:
            user_id = statement["actor"]["account"]["name"]
        else:
            user_id = statement["actor"]["mbox"]
        user_ids.add(user_id)
        activity_results[activity_id_for_remote[object_id]][user_id] = statement

    return activity_results, user_ids
