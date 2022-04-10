"""
The database definition of an activity
"""
import uuid
from flask import current_app
from flask_restplus import abort
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableDict

from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class ActivityType(db.Model):
    __tablename__ = "activity_type"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(32))


class ActivityRelationType(db.Model):
    __tablename__ = "activity_relation_type"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(32))


class ActivityRelation(db.Model):
    __tablename__ = "activity_relation"

    head_activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False, primary_key=True)
    head_activity = db.relationship("Activity", foreign_keys=[head_activity_id])
    tail_activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False, primary_key=True)
    tail_activity = db.relationship("Activity", foreign_keys=[tail_activity_id])

    type_id = db.Column(db.Integer, db.ForeignKey("activity_relation_type.id"), nullable=False)
    type = db.relationship("ActivityRelationType")

    properties = db.Column(db.JSON(), nullable=False, default=lambda: {})


def generate_uuid():
    return str(uuid.uuid4())


class ActivityAttachment(BaseModel):
    __tablename__ = "activity_attachment"

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100))
    extension = db.Column(db.String(32))

    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False)
    activity = db.relationship("Activity")

    @property
    def filename(self):
        return f"{self.name}.{self.extension}"

    @property
    def source_url(self):
        """
        The url external services will use to retreive the attachment
        """
        conf = current_app.config
        base_url = f"https://{conf.get('BASE_URL')}:{conf.get('PUBLIC_PORT_HTTPS')}/{conf.get('API_PUBLIC_POSTFIX')}"
        return f"{base_url}/{self.activity.collection_id}/activities/attachment/{self.uuid}"


class Activity(BaseModel):
    """
    Any activity that a user can participate in.
    Fields:
        :attr id: The unique identifier of activity
        :attr remote_id: Identifier used to link activity to entity on external platform
        :attr title: Title of the acitivity
        :attr type: Type of activity. Examples: exam, question, video, book section
    Relationships:
        :attr collection_id: The collection the activity belongs to
        backref
        :attr collection: The collection the activity belongs to
    """
    __tablename__ = "activity"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    remote_id = db.Column(db.String(100))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))
    type_id = db.Column(db.Integer, db.ForeignKey("activity_type.id"), nullable=True)
    type = db.relationship("ActivityType")
    visibility = db.Column(db.String(8))
    properties = db.Column(MutableDict.as_mutable(db.JSON), nullable=False, default=lambda: {})

    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=False)
    collection = db.relationship("Collection")

    attachments = db.relationship("ActivityAttachment", cascade="all, delete-orphan")

    constructs = db.relationship("Construct", secondary="construct_activity")

    construct_relations = db.relationship("ConstructActivity", cascade="all, delete")

    head_activities = db.relationship(
        "Activity",
        secondary="activity_relation",
        primaryjoin=id == ActivityRelation.tail_activity_id,
        secondaryjoin=id == ActivityRelation.head_activity_id)

    tail_activities = db.relationship(
        "Activity",
        secondary="activity_relation",
        primaryjoin=id == ActivityRelation.head_activity_id,
        secondaryjoin=id == ActivityRelation.tail_activity_id)

    head_relations = db.relationship(
        "ActivityRelation",
        primaryjoin=id == ActivityRelation.tail_activity_id,
        cascade="all, delete")

    tail_relations = db.relationship(
        "ActivityRelation",
        primaryjoin=id == ActivityRelation.head_activity_id,
        cascade="all, delete")

    @property
    def id_for_remote(self):
        """
        Returns the remote id without the prefix
        """
        string = self.remote_id
        string.split("_")
        return string[1]

    @classmethod
    def load_result(cls, activity_id):
        """
        Loads the results for an activity from its external source
        """
        from learnlytics.database.connector.connector import Connector

        activity = cls.get(activity_id, required=True)

        if activity.type.name == "exam":
            print(activity.title, activity_id, activity.remote_id)
            if activity.remote_id is None:
                abort(400, "The given activity is not connected to an external system")
            external_code = "_".join(activity.remote_id.split("_")[:-1])

            connector = Connector.get_code(external_code, required=True)

            return connector.model.get_results(activity)

    @classmethod
    def load_candidates(cls, activity_id):
        """
        Loads the persons for the exam so that results can be linked to users
        """
        from learnlytics.database.connector.connector import Connector

        activity = cls.get(activity_id, required=True)

        if activity.type.name == "exam":
            print(activity.title, activity_id, activity.remote_id)
            if activity.remote_id is None:
                abort(400, "The given activity is not connected to an external system")

            if "_" in activity.remote_id:
                external_code = "_".join(activity.remote_id.split("_")[:-1])
            else:
                external_code = activity.remote_id

            connector = Connector.get_code(external_code, required=True)

            return connector.model.load_candidates(activity)

    @property
    def lrs_object_id(self):
        from learnlytics.database.connector.connector import Connector

        if self.remote_id is None:
            # default to local code
            external_code = "local"
        else:
            if "_" in self.remote_id:
                external_code = "_".join(self.remote_id.split("_")[:-1])
            else:
                if self.remote_id == "local":
                    external_code = "local"
                else:
                    return self.remote_id

        connector = Connector.get_code(external_code)
        if connector is None:
            return self.remote_id

        return connector.model.get_lrs_object_id(self)

    @staticmethod
    def get_activity_types():
        activity_types = ActivityType.query.all()
        return Activity._activity_types_to_dict(activity_types)

    @staticmethod
    def get_activity_relation_types():
        activity_types = ActivityRelationType.query.all()
        return Activity._activity_types_to_dict(activity_types)

    @staticmethod
    def get_material_types():
        activity_types = ActivityType.query.filter(ActivityType.name.like('material%')).all()
        return Activity._activity_types_to_dict(activity_types)

    @staticmethod
    def get_survey_type():
        return Activity._activity_type_to_dict(ActivityType.query.filter(ActivityType.name == "survey").one_or_none())

    @staticmethod
    def get_visibility_types():
        return [
            {
                "id": 1,
                "value": 'T',
                "name": "visibility.t"
            },
            {
                "id": 2,
                "value": 'F',
                "name": "visibility.f"
            }
        ]

    @staticmethod
    def _activity_type_to_dict(activity_type):
        if activity_type is None:
            return None

        return {
            "id": activity_type.id,
            "name": activity_type.name
        }

    @staticmethod
    def _activity_types_to_dict(activity_types):
        result = []
        for activity_type in activity_types:
            result.append(Activity._activity_type_to_dict(activity_type))

        return result
