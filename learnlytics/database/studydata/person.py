"""
The database definition of a person
"""
from flask_restplus import abort

from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class Person(BaseModel):
    """
    Person contains information over a user from a single external data source
    Fields:
        :attr id: Unique identifier for person
        :attr remote_id: Identifier used to link person to entity on external platform
        :attr person_name:
        :attr display_name:
        :attr mail:
        :attr role:
    Relationships:
        :attr user, user_id: The user person pertains to (many-to-one relationship)
    """
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    remote_id = db.Column(db.String(100))
    person_name = db.Column(db.String(100))
    display_name = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    institution_id = db.Column(db.String(100))
    role = db.Column(db.String(100))
    lrs_actor = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", back_populates="persons")

    @classmethod
    def get_from_remote_id(cls, remote_id):
        """
        :param remote_id: The remote_id for which we want to know the id
        :param course: The course that the person is connected to
        :return: the internal id
        """
        return db.session.query(cls).filter(cls.remote_id == remote_id).one_or_none()

    def get_lrs_actor(self):
        from learnlytics.database.connector.connector import Connector

        if self.remote_id is None:
            abort(400, "The given person is not connected to an external system")
        if "_" in self.remote_id:
            external_code = "_".join(self.remote_id.split("_")[:-1])
        else:
            external_code = self.remote_id
        connector = Connector.get_code(external_code, required=True)

        return connector.model.get_lrs_actor(self)
