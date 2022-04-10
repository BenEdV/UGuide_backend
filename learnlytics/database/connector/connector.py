"""
The database definition of a Connector Settings
"""

from flask_restplus import abort
from sqlalchemy import event
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import JSONB

from learnlytics.connectors.remindo.model import RemindoModel
from learnlytics.connectors.learninglocker.model import LearningLockerModel
from learnlytics.connectors.local.model import LocalModel
from learnlytics.connectors.lrs.model import LRSModel
from learnlytics.connectors.xapi_moodle.model import MoodleXapiModel
from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


model_classes = {
    "remindo": RemindoModel,
    "learninglocker": LearningLockerModel,
    "local": LocalModel,
    "lrs": LRSModel,
    "hvp": MoodleXapiModel
}


class Connector(BaseModel):
    """
    An object to control permissions for external resources
    """
    __tablename__ = "connector"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    title = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)
    implementation = db.Column(db.String(100))
    settings = db.Column(JSONB)
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=False)
    collection = db.relationship("Collection")

    @property
    def model(self):
        if self._model is None:
            model_class = model_classes[self.implementation]
            self._model = model_class(self)
        return self._model

    def __init__(self, title, code, implementation, settings, collection_id=None):  # pylint: disable=redefined-builtin
        """
        :attr collection_parent_id: The id of the parent collection this would likely be the study collection
            such as "biology"
        """
        super(Connector, self).__init__()
        self.title = title
        self.code = code
        self.implementation = implementation
        self.settings = settings
        self._model = None

        from learnlytics.database.authorization.collection import Collection
        if collection_id is None:
            self.collection_id = Collection.get_root_collection(required=True).id
        else:
            self.collection_id = collection_id

    @validates("code")
    def _validate_code(self, key, code):  # pylint: disable=unused-argument, no-self-use, invalid-name
        """
        Function that validates a connector code
        """
        if " " in code:
            assert False, "connector code may not contain spaces"
        return code

    @classmethod
    def get_code(cls, code, required=False):
        """
        returns collection object with given name
        """
        connector = cls.query.filter(cls.code == code).one_or_none()
        if not connector and required:
            abort(404, message=f"Connector with code: {code} not found.")

        return connector

    def get_info(self):
        """
        Gets a dictionary with information about the given connector. The authorization of what information may be seen
        is handled in the module of the connector
        """
        model_class = model_classes[self.implementation]
        model = model_class(self)
        info_dict = model.get_info()
        info_dict["id"] = self.id
        info_dict["type"] = self.implementation

        return info_dict


@event.listens_for(Connector, "load")
def set_private_after_load(target, context):
    target._model = None
