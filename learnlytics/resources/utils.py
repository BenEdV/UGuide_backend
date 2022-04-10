# coding=utf-8
"""
This module contains utility functions
"""

from sqlalchemy.sql import and_, func
from create_api import utilns as ns
from flask_restplus import Resource

from learnlytics.authentication import auth_required
from learnlytics.extensions import db
from learnlytics.database.authorization.user import User
import learnlytics.database.studydata as md


@ns.route('/helloworld')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class HelloWorldResource(Resource):
    """
    This class for the hello world test.
    """

    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        A test call that can be used to test availablity and performance
        """

        return {"Hello": "World"}


@ns.route('/helloworld/auth')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class HelloWorldResource(Resource):
    """
    This class for the hello world test that only goes if the user is authorized.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        A test call that can be used to test availablity and performance
        """

        return {"Hello": "World authorized"}


@ns.route('/helloworld/db/<int:num_light_calls>/<int:num_medium_calls>/<int:num_heavy_calls>')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
@ns.doc(params={"num_calls": "The number of calls made to database"})
class HelloWorldResource(Resource):
    """
    This class for the hello world test that only goes if the user is authorized.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, num_light_calls, num_medium_calls, num_heavy_calls):  # pylint: disable=no-self-use
        """
        A test call that can be used to test availablity and performance
        """
        import itertools

        for _ in itertools.repeat(None, num_light_calls):
            db.engine.execute("SELECT 1 AS is_alive;")
        for _ in itertools.repeat(None, num_medium_calls):
            _ = md.Course.query.all()
        for _ in itertools.repeat(None, num_heavy_calls):
            course_exam_ids = [1, 2, 3, 4, 5]
            _ = md.Question.query.filter(md.Question.exam_id.in_(course_exam_ids)).all()

        return {"Hello": "World database"}


def calculate_percentile(exam_id, grade):
    """
    Calculate the percentile score for given exam and grade
    :param exam_id: Id of the exam
    :param grade: Grade
    :return: Percentile
    """
    low_gr = len(md.ExamResult.query.filter(and_(md.ExamResult.exam_id == exam_id,
                                                 md.ExamResult.grade < grade)).all())
    eq_gr = len(md.ExamResult.query.filter(and_(md.ExamResult.exam_id == exam_id,
                                                md.ExamResult.grade == grade)).all())
    all_gr = len(md.ExamResult.query.filter(md.ExamResult.exam_id == exam_id).all())
    return str(((2 * low_gr + eq_gr) * 50) / all_gr)


def calculate_course_percentile(course_id, user_id):
    """
    Calculate the percentile score for given course and student
    :param course_id: Id of the course
    :param user_id: Id of the user
    :return: Percentile
    """
    user = User.query.filter(User.id == user_id).one_or_none()
    grade = user.grade_for_course(course_id)
    if grade is None:
        return None

    grades = []
    users = md.Course.query.get(course_id).users.all()
    for user in users:
        grades.append(user.grade_for_course(course_id))

    return calculate_percentile_list(grade, grades)


def calculate_percentile_list(grade, grades):
    """
    Calculate the percentile for given grade and list of grades
    :param grade: Grade
    :param grades: List of grades
    :return: Percentile
    """
    if grade is None:
        return None
    low_gr = len([x for x in grades if x is None or x < grade])
    eq_gr = len([x for x in grades if x == grade])
    all_gr = len(grades)
    return str(((2 * low_gr + eq_gr) * 50) / all_gr)
