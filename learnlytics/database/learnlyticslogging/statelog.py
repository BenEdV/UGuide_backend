"""
The database definition of state logging
"""

from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


class EventLog(BaseModel):
    """
    Saves information about the state change for the current user
    Fields:
        :attr id: Unique identifier for logging entry
        :attr user_id: The id of the current user
        :attr from_state: The app.routes.js state from which the user came
        :attr to_state: The app.routes.js state to which the user is going
        :attr details: Parameters regarding the state change
        :attr timestamp: Timestamp of when the redirect triggered
    """
    __tablename__ = "event_log"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    session_id = db.Column(db.String(64))
    subsession = db.Column(db.Integer)
    details = db.Column(db.JSON)
    parameters = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime(timezone=True))

    state_id = db.Column(db.Integer, db.ForeignKey("event_state.id", ondelete="CASCADE", onupdate="CASCADE"))
    state = db.relationship("EventState")
    subject_id = db.Column(db.Integer, db.ForeignKey("event_subject.id", ondelete="CASCADE", onupdate="CASCADE"))
    subject = db.relationship("EventSubject")
    type_id = db.Column(db.Integer, db.ForeignKey("event_type.id", ondelete="CASCADE", onupdate="CASCADE"))
    e_type = db.relationship("EventType")


class EventState(db.Model):
    __tablename__ = "event_state"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)


class EventSubject(db.Model):
    __tablename__ = "event_subject"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)


class EventType(db.Model):
    __tablename__ = "event_type"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
