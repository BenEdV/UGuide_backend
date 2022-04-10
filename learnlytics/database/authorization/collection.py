"""
The database definition of a collection
"""
from sqlalchemy.ext.associationproxy import association_proxy
from flask import current_app
from flask_restplus import abort

from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class Collection(BaseModel):
    """
    This class contains the definition for a Collection
    :attr parent_id: Collection has a hierarchical structure, Users with a Role for a Collection
        have the same role for the children of that Collection.
    """
    __tablename__ = "collection"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("collection.id", ondelete="CASCADE"), nullable=True)
    parent = db.relationship("Collection", remote_side=[id])
    children = db.relationship(
        "Collection", back_populates="parent", lazy="dynamic", cascade="all, delete", passive_deletes=True)
    settings = db.Column(db.JSON, nullable=False, default=lambda: {})

    course_instance = db.relationship("CourseInstance", cascade="all, delete", uselist=False,
                                      back_populates="collection")
    course_instance_id = association_proxy("course_instance", "id")

    user_roles = db.relationship("UserRole", lazy="dynamic", cascade="all, delete-orphan")
    all_users = association_proxy("user_roles", "user")
    all_user_ids = association_proxy("user_roles", "user_id")

    construct_models = db.relationship("ConstructModel", lazy="dynamic", cascade="all, delete-orphan")
    activities = db.relationship("Activity", lazy="dynamic", cascade="all, delete-orphan")
    activity_ids = association_proxy("activities", "id")
    connectors = db.relationship("Connector", lazy="dynamic", cascade="all, delete-orphan")

    @property
    def members(self):
        from learnlytics.database.authorization.user import User, UserRole
        from learnlytics.database.authorization.role import Role

        members = User.query.\
            join(UserRole, UserRole.user_id == User.id).\
            filter(UserRole.collection_id == self.id).\
            join(Role, UserRole.role_id == Role.id).\
            filter(Role.name == "member").all()

        return members

    @property
    def member_ids(self):
        from learnlytics.database.authorization.user import User, UserRole
        from learnlytics.database.authorization.role import Role

        member_ids = db.session.query(User.id).\
            join(UserRole, UserRole.user_id == User.id).\
            filter(UserRole.collection_id == self.id).\
            join(Role, UserRole.role_id == Role.id).\
            filter(Role.name == "member").all()

        return [m.id for m in member_ids]

    @property
    def member_count(self):
        from learnlytics.database.authorization.user import UserRole
        from learnlytics.database.authorization.role import Role

        count = UserRole.query.\
            join(Role, UserRole.role_id == Role.id).\
            filter(UserRole.collection_id == self.id).\
            filter(Role.name == "member").count()

        return count

    @classmethod
    def get_name(cls, name, required=False):
        """
        returns collection object with given name
        """
        collection = cls.query.filter(cls.name == name).one_or_none()
        if not collection and required:
            abort(404, message=f"Collection with name: {name} not found.")

        return collection

    def get_hierarchy_info(self):
        """
        Function that turns entire hierarchy below this object into a nested dictionary with info of each object
        :return: Dictionary with info on this object and nested dictionaries with info of collection belows this object
        """
        info = {
            "id": self.id,
            "name": self.name
        }

        if self.course_instance:
            info["course"] = {
                "id": self.course_instance.course_id,
                "name": self.course_instance.course.name
            }
            info["period"] = {
                "id": self.course_instance.period_id,
                "name": self.course_instance.period.name
            }

        children = self.children.all()
        if children is not None and len(children) > 0:
            subs = [k for k in (sub.get_hierarchy_info() for sub in children)]
            info["sub"] = subs
        return info

    @classmethod
    def get_root_collection(cls, required=False):
        """
        return the root collection of the collection tree
        """
        return cls.get(1, required=required)

    def main_lrs_connector(self):
        for connector in self.connectors:
            if connector.implementation == "lrs" and connector.settings["main"]:
                return connector

        return None

    def create_lrs_for_collection(self, title, main):
        from learnlytics.database.connector.connector import Connector

        ll_connector = Connector.get_code("learninglocker", required=True)
        (store, internal_credentials) = ll_connector.model.create_new_store(title)
        external_credentials = ll_connector.model.create_new_client(
            "External key",
            store["_id"],
            ["statements/write", "statements/read/mine"]
        )

        lrs_connector = Connector(
            title=title,
            code=f'lrs_{self.id}_{title.replace(" ", "_").lower()}',
            implementation="lrs",
            settings={
                "lrs_id": store["_id"],
                "xapi_base_url": ll_connector.settings["xapi_base_url"],
                "public_base_url":
                    f"https://{current_app.config.get('BASE_URL')}/{current_app.config.get('XAPI_PUBLIC_POSTFIX')}",
                "clients": [
                    {
                        "key": internal_credentials["key"],
                        "secret": internal_credentials["secret"],
                        "scopes": internal_credentials["scopes"]
                    },
                    {
                        "key": external_credentials["key"],
                        "secret": external_credentials["secret"],
                        "scopes": external_credentials["scopes"]
                    }
                ],
                "main": main,
                "api_version": "1.0.3"
            },
            collection_id=self.id
        )
        db.session.add(lrs_connector)

        return lrs_connector


class UserCollectionSettings(db.Model):
    __tablename__ = "user_collection_settings"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collection.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    settings = db.Column(db.JSON, nullable=False, default=lambda: {})
