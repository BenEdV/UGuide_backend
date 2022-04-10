"""
The database definition of a permission
"""
from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class Permission(BaseModel):
    """
    This class contains the definition for a permission that a role can have
    """
    __tablename__ = "permission"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
