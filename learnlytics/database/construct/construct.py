"""
The database definition of a thermos construct
"""
from sqlalchemy.ext.associationproxy import association_proxy

from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel
import learnlytics.database.studydata as md


class ConstructType(db.Model):
    __tablename__ = "construct_type"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(32))


class ConstructRelationType(db.Model):
    __tablename__ = "construct_relation_type"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(32))


class ConstructRelation(db.Model):
    __tablename__ = "construct_relation"

    head_construct_id = db.Column(db.Integer, db.ForeignKey("construct.id"), nullable=False, primary_key=True)
    tail_construct_id = db.Column(db.Integer, db.ForeignKey("construct.id"), nullable=False, primary_key=True)

    type_id = db.Column(db.Integer, db.ForeignKey("construct_relation_type.id"), nullable=False)
    type = db.relationship("ConstructRelationType")

    properties = db.Column(db.JSON(), nullable=False, default=lambda: {})


class ConstructActivityRelationType(db.Model):
    __tablename__ = "construct_activity_relation_type"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(32))


class ConstructActivity(db.Model):
    __tablename__ = "construct_activity"

    construct_id = db.Column(db.Integer, db.ForeignKey("construct.id"), nullable=False, primary_key=True)
    construct = db.relationship("Construct")
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False, primary_key=True)
    activity = db.relationship("Activity")

    type_id = db.Column(db.Integer, db.ForeignKey("construct_activity_relation_type.id"), nullable=False)
    type = db.relationship("ConstructActivityRelationType")

    properties = db.Column(db.JSON(), nullable=False, default=lambda: {})


class Construct(BaseModel):
    """
    A construct
    Fields:
        :attr id: Unique identifier of the construct
        :attr title: The name of the construct
    """
    __tablename__ = "construct"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type_id = db.Column(db.Integer, db.ForeignKey("construct_type.id"), nullable=False)
    type = db.relationship("ConstructType")

    properties = db.Column(db.JSON(), nullable=False, default=lambda: {})

    model_id = db.Column(db.Integer, db.ForeignKey("construct_model.id", ondelete="CASCADE"))
    model = db.relationship("ConstructModel", back_populates="constructs")

    collection_id = association_proxy("model", "collection_id")
    collection = association_proxy("model", "collection")

    activities = db.relationship("Activity", secondary="construct_activity")

    activity_relations = db.relationship("ConstructActivity", cascade="all, delete")

    head_constructs = db.relationship(
        "Construct",
        secondary="construct_relation",
        primaryjoin=id == ConstructRelation.tail_construct_id,
        secondaryjoin=id == ConstructRelation.head_construct_id)

    tail_constructs = db.relationship(
        "Construct",
        secondary="construct_relation",
        primaryjoin=id == ConstructRelation.head_construct_id,
        secondaryjoin=id == ConstructRelation.tail_construct_id)

    head_relations = db.relationship(
        "ConstructRelation",
        primaryjoin=id == ConstructRelation.tail_construct_id,
        cascade="all, delete")

    tail_relations = db.relationship(
        "ConstructRelation",
        primaryjoin=id == ConstructRelation.head_construct_id,
        cascade="all, delete")

    @classmethod
    def get_name(cls, name):
        """
        returns construct object with given name
        """
        return cls.query.filter(cls.name == name).one_or_none()


class ConstructModel(BaseModel):
    """
    A model
    Fields:
        :attr id: Unique identifier of the construct
        :attr title: The name of the construct
    """
    __tablename__ = "construct_model"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    method = db.Column(db.String(100))
    cached_values = db.Column(db.JSON, nullable=True)
    parameters = db.Column(db.JSON, nullable=True)

    constructs = db.relationship(
        "Construct", back_populates="model", lazy="dynamic", cascade="all, delete-orphan", passive_deletes=True)
    construct_ids = association_proxy("constructs", "id")

    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=False)
    collection = db.relationship("Collection")

    __implementation_model = None
    from learnlytics.models.construct_models.mean_model.update_scores import MeanModel
    from learnlytics.models.construct_models.thermos_model.update_scores import ThermosModel

    __implementation_models = {
        MeanModel.method: MeanModel,
        ThermosModel.method: ThermosModel
    }

    @property
    def implementation_model(self):
        if self.__implementation_model:
            return self.__implementation_model

        self.__implementation_model = self.__implementation_models[self.method](model_id=self.id)
        return self.__implementation_model

    @classmethod
    def get_name(cls, name):
        """
        returns construct object with given name
        """
        return cls.query.filter(cls.name == name).one_or_none()

    def add_construct(self, construct_id):
        construct = md.Concept.get(construct_id)
        self.constructs.append(construct)
        self.implementation_model.init_new_construct_scores(construct_id, construct.courses[0].id)

    @staticmethod
    def get_all_types():
        result = []
        for model_name, model in ConstructModel.__implementation_models.items():
            result_model = {
                "name": model_name,
            }
            construct_type_names = model.supported_construct_types
            construct_types = ConstructType.query.filter(ConstructType.name.in_(construct_type_names))
            for construct_type in construct_types:
                result_model[construct_type.name] = construct_type.id

            result.append(result_model)

        return result

    @staticmethod
    def get_construct_relation_types():
        construct_relation_types = ConstructRelationType.query.all()
        return ConstructModel._construct_type_to_dict(construct_relation_types)

    @staticmethod
    def get_construct_activity_relation_types():
        construct_activity_relations = ConstructActivityRelationType.query.all()
        return ConstructModel._construct_type_to_dict(construct_activity_relations)

    def get_types(self):
        construct_type_names = self.implementation_model.supported_construct_types
        construct_types = ConstructType.query.filter(ConstructType.name.in_(construct_type_names))
        result = []
        for construct_type in construct_types:
            result.append({
                "id": construct_type.id,
                "name": construct_type.name
            })

        return result

    @staticmethod
    def _construct_type_to_dict(construct_types):
        result = []
        for construct_type in construct_types:
            result.append({
                "id": construct_type.id,
                "name": construct_type.name
            })

        return result

    @staticmethod
    def _head_constructs_to_dict(head_relations):
        result = []
        for head_relation in head_relations:
            relation_dict = {
                "id": head_relation.head_construct_id,
                "relation_type": head_relation.type.name,
                "relation_properties": head_relation.properties
            }
            result.append(relation_dict)

        return result

    @staticmethod
    def _tail_constructs_to_dict(tail_relations):
        result = []
        for tail_relation in tail_relations:
            relation_dict = {
                "id": tail_relation.tail_construct_id,
                "relation_type": tail_relation.type.name,
                "relation_properties": tail_relation.properties
            }
            result.append(relation_dict)

        return result
