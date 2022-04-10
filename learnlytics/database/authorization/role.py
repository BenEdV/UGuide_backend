"""
The database definition of a role
"""
from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel
from flask import abort


class Role(BaseModel):
    """
    This class contains the definition for a Role that a User can have for a Collection
    """
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(100))
    permissions = db.relationship("Permission", secondary="role_permissions", lazy="dynamic")

    @classmethod
    def get_name(cls, name, required=False):
        """
        returns role object with given name
        """
        role = cls.query.filter(cls.name == name).one_or_none()
        if not role and required:
            abort(404, f"Role with name: {name} not found.")

        return role

    @classmethod
    def get_all_names(cls):
        """
        Returns the names of all supported roles
        """
        roles = cls.query.all()
        return [role.name for role in roles]

    def get_permission_names(self):
        """
        Returns an array of strings being the names of the permissions attributed to the role
        """
        permission_names = []
        for permission in self.permissions:
            permission_names.append(permission.name)
        return permission_names


class RolePermission(db.Model):
    """
    A given role has a set of permissions
    """
    __tablename__ = "role_permissions"

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    permission_id = db.Column(
        db.Integer,
        db.ForeignKey("permission.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
