"""
The database definition of storing user settings
"""

from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class UserSettings(BaseModel):
    """
    Used to save user settings
    Fields:
        :attr id: Unique identifier for the user settings
        :attr user_id: The id of the current user
        :attr course_id: The course to which the preferences apply
        :attr preferences: JSON string in which the preferences are stored
    """
    __tablename__ = "user_settings"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    preferences = db.Column(db.JSON)
