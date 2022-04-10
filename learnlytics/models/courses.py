"""
This module contains the model for courses
"""
from flask_restplus import abort
import sqlalchemy
from learnlytics.authorization.manager import authorize
from learnlytics.extensions import db
import learnlytics.database.studydata as md


# pylint: disable=no-member
class Courses(object):  # pylint: disable=no-init
    """
    This class contains methods to get, add delete courses
    """

    @staticmethod
    def get_course(course):
        """
        Gets a course with the given course_id.
        :param course_id: id of the the course to get
        :return: a json of the requested course.
        """
        result_dic = {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
        return result_dic

    @staticmethod
    def get_courses():
        """
        Gets a list of all available courses.
        :return: a list of json objects of all the available courses.
        """
        courses = md.Course.query.all()
        result = []
        for queried_course in courses:
            course = Courses.get_course(queried_course)
            result.append(course)
        return result

    @staticmethod
    def add_course(name, code):
        """
        Adds a new course to the database
        """
        if len(name) > md.Course.name.type.length:
            abort(400, f"Given name for course is longer than maximum of {md.Course.name.type.length} characters")
        if len(code) > md.Course.code.type.length:
            abort(400, f"Given code for course is longer than maximum of {md.Course.code.type.length} characters")

        course = md.Course(
            name=name,
            code=code
        )

        try:
            db.session.add(course)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            abort(409, message=f"Course with code: {code} already exists.")

        return Courses.get_course(course)

    @staticmethod
    def delete_course(course):
        """
        Deletes a course with the given course_id.
        :param course: The course to delete.
        """
        db.session.delete(course)
        db.session.commit()
