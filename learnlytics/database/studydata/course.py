"""
The database definition of a course
"""

from flask_restplus import abort
from sqlalchemy.orm import validates

from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class CourseInstance(BaseModel):
    __tablename__ = "course_instance"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name

    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=False, unique=True)
    collection = db.relationship("Collection", back_populates="course_instance")

    period_id = db.Column(db.Integer, db.ForeignKey("period.id"), nullable=False)
    period = db.relationship("Period")

    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    course = db.relationship("Course")

    def __init__(self, course, period, collection=None, parent_collection_id=None):  # pylint: disable=redefined-builtin
        """

        """
        from learnlytics.database.authorization.collection import Collection
        super(CourseInstance, self).__init__()
        self.course = course
        self.period = period
        if collection is None:
            self.collection = Collection(name=f"{course.name} {period.name}", parent_id=parent_collection_id)
            db.session.add(self.collection)
        else:
            self.collection = collection
        db.session.flush()

        self.collection.create_lrs_for_collection(title=f"{self.course.code}_{self.period.id}", main=True)


class Period(BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name

    name = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    instances = db.relationship(
        "CourseInstance", back_populates="period", lazy="dynamic", cascade="delete", passive_deletes=True)


class Course(BaseModel):
    """
    Entity for a Course,
    Fields:
        :attr name: The name of the course
    Relationships:
        :attr instances: The instances of course. These can have different students, instructors and activities
    """
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(16), unique=True, nullable=False)

    instances = db.relationship(
        "CourseInstance", back_populates="course", lazy="dynamic", cascade="delete", passive_deletes=True)

    def __init__(self, name, code):  # pylint: disable=redefined-builtin
        """

        """
        super(Course, self).__init__()
        self.name = name
        self.code = code

    @validates("code")
    def _validate_code(self, key, code):  # pylint: disable=unused-argument, no-self-use, invalid-name
        """
        Function that validates a course code
        """
        if " " in code:
            assert False, "course code may not contain spaces"
        return code

    @classmethod
    def get_code(cls, code, required=False):
        """
        returns course object with given code
        """
        course = cls.query.filter(cls.code == code).one_or_none()
        if not course and required:
            abort(404, message=f"Course with code: {code} not found.")

        return course
