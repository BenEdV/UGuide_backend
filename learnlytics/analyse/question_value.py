import math
import numpy
from sqlalchemy.sql import func

from learnlytics.extensions import db
import learnlytics.database.studydata as md


def update_p_value(question):
    """
    Calculates the given p value for a question based on the results in the database
    """
    results = md.QuestionResult.query.filter(md.QuestionResult.question_id == question.id)
    total = results.count()
    if total == 0:
        question.value_p = 0
        return
    score_sum = db.session.query(func.sum(md.QuestionResult.score)).\
        filter(md.QuestionResult.question_id == question.id).\
        group_by(md.QuestionResult.question_id).scalar()
    p_value = float(score_sum) / (total * question.max_score)
    question.value_p = p_value


def update_std_value(question):
    """
    Calculates the given std value for a question based on the results in the database
    """
    results = md.QuestionResult.query.filter(md.QuestionResult.question_id == question.id)
    scores = [result.score for result in results]
    std_value = numpy.std(scores, ddof=1)
    if numpy.isnan(std_value):
        question.value_std = None
    else:
        question.value_std = std_value


def update_rit_value(question):
    """
    Calculates the given item total correlation (rit) value for a question based on the results in the database
    """
    correct_exams = md.ExamResult.query.join(md.ExamResult.question_results, aliased=True).\
        filter(md.QuestionResult.question_id == question.id, md.QuestionResult.score == question.max_score).all()
    correct_scores = [exam.score for exam in correct_exams]
    correct_average = numpy.mean(correct_scores)
    total_correct = float(len(correct_exams))

    incorrect_exams = md.ExamResult.query.join(md.ExamResult.question_results, aliased=True).\
        filter(md.QuestionResult.question_id == question.id, md.QuestionResult.score < question.max_score).all()

    incorrect_scores = [exam.score for exam in incorrect_exams]
    if not incorrect_scores:
        # No incorrect answers
        question.value_rir = 1.0
        return
    incorrect_average = numpy.mean(incorrect_scores)
    total_incorrect = float(len(incorrect_exams))

    scores = incorrect_scores + correct_scores
    std = numpy.std(scores, ddof=1)
    total = total_correct + total_incorrect

    rit_value = (correct_average - incorrect_average) / std * math.\
        sqrt((total_correct * total_incorrect) / (total * total))

    if numpy.isnan(rit_value):
        question.value_rit = None
    else:
        question.value_rit = rit_value


def update_rir_value(question):
    """
    Calculates the given item rest correlation (rir) value for a question based on the results in the database
    """
    no_questions = question.exam.questions.count()
    correct_exams = md.ExamResult.query.join(md.ExamResult.question_results, aliased=True).\
        filter(md.QuestionResult.question_id == question.id, md.QuestionResult.score == question.max_score).all()

    # Adjusts the scores based on the exclusion of the given question
    correct_scores = [(no_questions * exam.score - question.max_score) / (no_questions - 1) for exam in correct_exams]
    correct_average = numpy.mean(correct_scores)
    total_correct = float(len(correct_exams))

    incorrect_exams = md.ExamResult.query.join(md.ExamResult.question_results, aliased=True).\
        filter(md.QuestionResult.question_id == question.id, md.QuestionResult.score < question.max_score).all()

    incorrect_scores = [(no_questions * exam.score + question.max_score)/(no_questions - 1) for exam in incorrect_exams]
    if not incorrect_scores:
        # No incorrect answers
        question.value_rir = 1.0
        return
    incorrect_average = numpy.mean(incorrect_scores)
    total_incorrect = float(len(incorrect_exams))

    scores = incorrect_scores + correct_scores
    std = numpy.std(scores, ddof=1)
    total = total_correct + total_incorrect

    rir_value = (correct_average-incorrect_average) / std * math.sqrt((total_correct * total_incorrect)/(total * total))

    if numpy.isnan(rir_value):
        question.value_rir = None
    else:
        question.value_rir = rir_value
