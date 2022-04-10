"""
The database definition of a user
"""
from flask import current_app
from sqlalchemy.orm import validates

from learnlytics.authentication.providers.local_provider import LocalProvider
from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class UserRole(db.Model):
    """
    A User has a Role for a Collection
    """
    __tablename__ = "user_role"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    user = db.relationship("User")

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True)
    role = db.relationship("Role")

    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collection.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)


# pylint: disable=too-few-public-methods
class UserPassHash(db.Model):
    """
    This class contains the model of a hashed password and allows to hash a password
    """
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    hash = db.Column(db.String)

    def __init__(self, id, passw):
        self.user_id = id
        self.hash = LocalProvider.make_hash(passw.encode("utf-8")).decode("utf-8")

    def reset_password(self, new_password):
        self.hash = LocalProvider.make_hash(new_password.encode("utf-8")).decode("utf-8")
        db.session.commit()

    @classmethod
    def get_hash(cls, id):
        """
        :param id: The id to get the hash for
        :return: the passwordhash if it exists
        """
        obj = cls.query.get(id)
        if obj is not None:
            return str(obj.hash)


class UserToken(BaseModel):
    """
    Entity containing a token for a user
    """
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    identity_provider = db.Column(db.String(100), primary_key=True)
    token = db.Column(db.String(256))


# pylint: disable=too-few-public-methods
class User(BaseModel):
    """
    Entity containing personal and log-in information, and membership to courses
    Fields:
        :attr id: Unique identifier for user
        :attr idp: Key of IdentityProvider authenticating the user
        :attr salt: Randomly generated salt for password hashing
        :attr display_name: User's full name
        :attr mail: User's email address
        :attr analytics:
    Relationships:
        :attr persons: The persons of a user (one-to-many relationship)
        :attr courses, course_ids: The courses a user follows (many-to-many relationship)
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    display_name = db.Column(db.String(100))
    mail = db.Column(db.String(100), unique=True)
    institution_id = db.Column(db.String(100), unique=True)

    persons = db.relationship("Person", back_populates="user", lazy="dynamic")

    def __init__(self, institution_id=None, display_name=None, mail=None, first_name=None, last_name=None):
        assert institution_id is not None or mail is not None
        super(User, self).__init__()
        self.institution_id = institution_id
        self.display_name = display_name
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail

    def __repr__(self):
        return f"User(id={self.id}, display_name={self.display_name}, institution_id={self.institution_id})"

    @property
    def actor(self):
        actor = {
            "homePage": f"https://{current_app.config['BASE_URL']}/users",
            "name": str(self.id)
        }
        return actor

    def roles_for_collection(self, collection_id):
        from learnlytics.database.authorization.role import Role
        return Role.query.join(UserRole, Role.id == UserRole.role_id).\
            filter(UserRole.collection_id == collection_id, UserRole.user_id == self.id).\
            all()

    def collections_with_permissions(self, permissions):
        """
        Returns the set of collections for which the user has the given permissions
        """
        from learnlytics.database.authorization.collection import Collection
        from learnlytics.database.authorization.permission import Permission
        from learnlytics.database.authorization.role import Role, RolePermission
        collections = Collection.query.join(UserRole, UserRole.collection_id == Collection.id).\
            filter(UserRole.user_id == self.id).\
            join(Role, Role.id == UserRole.role_id).\
            join(RolePermission, RolePermission.role_id == Role.id).\
            join(Permission, Permission.id == RolePermission.permission_id).\
            filter(Permission.name.in_(permissions)).\
            all()

        return collections

    @validates('mail')
    def validate_mail(self, key, address):
        if address is None:
            return None
        assert '@' in address
        assert address == address.lower(), "Address contains capital letters, address must first be cast to lower"
        return address

    @validates('institution_id')
    def validate_instiution_id(self, key, new_institution_id):
        if new_institution_id is None:
            return None
        assert '@' not in new_institution_id, "institution_id cannot contain a capital letter to differentiate it from \
            mail"
        return new_institution_id

    def grade_for_course(self, course_id):
        """
        Function that returns the user's grade for the given course
        :param course_id: The id for the course
        :return: The grade
        """
        from learnlytics.database.studydata.exam_result import UserCourseScore
        score_object = UserCourseScore.query.filter(
            UserCourseScore.course_id == course_id,
            UserCourseScore.user_id == self.key).one_or_none()
        if score_object:
            return score_object.score

        return 0


# load authentication and authorization
def add_user(first_name, last_name, display_name, mail, institution_id):
    """
    Function that adds the user to the database
    :param first_name: first name of the user
    :param last_name: last name of the user
    :param display_name: name that will be displayed throughout the system
    :param mail: email of the user
    :param institution_id: The institutional code for the user, eg. 123456
    :return: User object that was added
    """
    _user = User(first_name=first_name,
                 last_name=last_name,
                 display_name=display_name,
                 institution_id=institution_id,
                 mail=mail)
    db.session.add(_user)
    db.session.commit()
    return _user


def load_user(id):
    """
    Function that loads the user based on id
    :param name: id of the user
    :return: User object if it exists else None
    """
    if isinstance(id, int):
        user = User.query.filter(User.id == id).one_or_none()
        return user

    user = User.query.filter(User.institution_id == id).one_or_none()
    if user:
        return user

    user = User.query.filter(User.mail == id.lower()).one_or_none()
    if user:
        return user


def payload_ext(payload, identity):
    """
    Function that adds extra information to the token payload information
    :param payload: payload with basic information
    :param identity: Authenticated user object
    :return: payload parameter with extra information
    """
    payload["display_name"] = identity.display_name
    payload["mail"] = identity.mail
    return payload
