"""
The database definition of reqlogging requests
"""

from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class RequestLog(BaseModel):
    """
    Used to log requests to the backend
    Fields:
        :attr id: Unique identifier for logging entry
        :attr user_id: The id of the current user
        :attr from_state: The app.routes.js state from which the user came
        :attr to_state: The app.routes.js state to which the user is going
        :attr details: Description of the event
        :attr timestamp: Timestamp of when the redirect triggered
    """
    __tablename__ = "request_log"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    time = db.Column(db.DateTime(timezone=True))
    request_path = db.Column(db.String(200))
    request_method = db.Column(db.String(10))
