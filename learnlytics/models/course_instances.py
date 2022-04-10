"""
This module contains the model for courses
"""

from learnlytics.authentication.util import current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.user import UserRole
from learnlytics.extensions import db
import learnlytics.database.studydata as md


# pylint: disable=no-member
class CourseInstances(object):  # pylint: disable=no-init
    """
    This class contains methods to get, add delete courses
    """

    @staticmethod
    def get_course_instance(course_instance_id):
        """
        Gets a course with the given course_id.
        :param course_id: id of the the course to get
        :return: a json of the requested course.
        """
        course_instance = md.CourseInstance.get(course_instance_id, required=True)
        result_dic = CourseInstances._course_instance_dict(course_instance)
        return result_dic

    @staticmethod
    def _course_instance_dict(course_instance):
        return {
            "id": course_instance.id,
            "collection_id": course_instance.collection_id,
            "period": {
                "id": course_instance.period.id,
                "name": course_instance.period.name,
                "start_date":
                    course_instance.period.start_date.isoformat() if course_instance.period.start_date else None,
                "end_date": course_instance.period.end_date.isoformat() if course_instance.period.end_date else None
            },
            "course": {
                "id": course_instance.course.id,
                "name": course_instance.course.name,
                "code": course_instance.course.code
            }
        }

    @staticmethod
    def get_course_instances():
        """
        Gets a list of all available courses.
        :return: a list of json objects of all the available courses.
        """
        course_instances = db.session.query(md.CourseInstance).\
            join(Collection, Collection.id == md.CourseInstance.collection_id).\
            join(UserRole, UserRole.collection_id == Collection.id).\
            filter(UserRole.user_id == current_identity().id).all()
        result = []
        for course_instance in course_instances:
            course_instance_dict = CourseInstances._course_instance_dict(course_instance)
            result.append(course_instance_dict)
        return result

    @staticmethod
    def get_course_instances_for_period(period_id):
        """
        Gets a list of all available courses.
        :return: a list of json objects of all the available courses.
        """
        course_instances = db.session.query(md.CourseInstance).\
            filter(md.CourseInstance.period_id == period_id).\
            join(Collection, Collection.id == md.CourseInstance.collection_id).\
            join(UserRole, UserRole.collection_id == Collection.id).\
            filter(UserRole.user_id == current_identity().id).all()
        result = []
        for course_instance in course_instances:
            course_instance_dict = CourseInstances._course_instance_dict(course_instance)
            result.append(course_instance_dict)
        return result

    @staticmethod
    def add_course_instance(course_id, period_id, parent_collection_id, collection):
        """
        Adds a new course instance to the database
        """
        course = md.Course.get(course_id, required=True)
        period = md.Period.get(period_id, required=True)

        course_instance = md.CourseInstance(
            course=course,
            period=period,
            parent_collection_id=parent_collection_id,
            collection=collection
        )

        db.session.add(course_instance)
        # Give creator of the course an admin role for the course instance, if a new collection has been made
        if parent_collection_id is not None:
            import learnlytics.authorization.manager as auth
            from learnlytics.database.authorization.role import Role
            admin_role = Role.get_name("admin")

            auth.add_user_role(current_identity().id, admin_role.id, course_instance.collection_id)

        db.session.commit()

        return CourseInstances._course_instance_dict(course_instance)

    @staticmethod
    def delete_course_instance(course_instance):
        """
        Deletes a course with the given course_id.
        :param course: The course to delete.
        """
        db.session.delete(course_instance)
        db.session.commit()
