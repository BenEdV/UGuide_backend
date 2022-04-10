"""
Gives a user or a collection of users a construct score for an activity at a specific time. If the activity_id is
NULL this implies that the score is for the entire collection of which the construct is a part of.
"""

from sqlalchemy import func, and_, desc
from learnlytics.extensions import db


def new_construct_score(user_id, construct_id, timestamp, activity_id, collection_id):
    if activity_id is None:
        if construct_id is None:
            latest_score = UserScore.query.\
                filter(UserScore.user_id == user_id).\
                filter(UserScore.collection_id == collection_id).\
                filter(UserScore.timestamp < timestamp).\
                order_by(desc(UserScore.timestamp)).\
                first()

            if latest_score is not None:
                score = latest_score.score
                max_score = latest_score.max_score
            else:
                score = 0
                max_score = 0

            score = UserScore(
                user_id=user_id,
                collection_id=collection_id,
                score=score,
                max_score=max_score,
                timestamp=timestamp
            )
            return score

        latest_score = UserConstructScore.query.\
            filter(UserConstructScore.user_id == user_id).\
            filter(UserConstructScore.construct_id == construct_id).\
            filter(UserConstructScore.timestamp < timestamp).\
            order_by(desc(UserConstructScore.timestamp)).\
            first()

        if latest_score is not None:
            score = latest_score.score
            max_score = latest_score.max_score
        else:
            score = 0
            max_score = 0

        score = UserConstructScore(
            user_id=user_id,
            construct_id=construct_id,
            score=score,
            max_score=max_score,
            timestamp=timestamp
        )
        return score

    latest_score = UserActivityConstructScore.query.\
        filter(UserActivityConstructScore.user_id == user_id).\
        filter(UserActivityConstructScore.activity_id == activity_id).\
        filter(UserActivityConstructScore.construct_id == construct_id).\
        filter(UserActivityConstructScore.timestamp < timestamp).\
        order_by(desc(UserActivityConstructScore.timestamp)).\
        first()

    if latest_score is not None:
        score = latest_score.score
        max_score = latest_score.max_score
    else:
        score = 0
        max_score = 0

    score = UserActivityConstructScore(
        user_id=user_id,
        activity_id=activity_id,
        construct_id=construct_id,
        score=score,
        max_score=max_score,
        timestamp=timestamp
    )
    return score


def new_collection_construct_score(collection_id, construct_id, timestamp, activity_id, score, max_score):
    if activity_id is None:
        if construct_id is None:
            score = CollectionScore(
                collection_id=collection_id,
                score=score,
                max_score=max_score,
                timestamp=timestamp
            )
            return score

        score = CollectionConstructScore(
            collection_id=collection_id,
            construct_id=construct_id,
            score=score,
            max_score=max_score,
            timestamp=timestamp
        )
        return score

    score = CollectionActivityConstructScore(
        collection_id=collection_id,
        activity_id=activity_id,
        construct_id=construct_id,
        score=score,
        max_score=max_score,
        timestamp=timestamp
    )
    return score


def get_scores(user_ids, construct_ids, activity_ids):
    scores = []
    uas = UserActivityConstructScore.query.\
        filter(UserActivityConstructScore.user_id.in_(user_ids)).\
        filter(UserActivityConstructScore.construct_id.in_(construct_ids)).\
        filter(UserActivityConstructScore.activity_id.in_(activity_ids)).all()
    scores.extend(uas)

    us = UserConstructScore.query.\
        filter(UserConstructScore.user_id.in_(user_ids)).\
        filter(UserConstructScore.construct_id.in_(construct_ids)).all()
    scores.extend(us)

    uis = UserScore.query.\
        filter(UserScore.user_id.in_(user_ids)).all()
    scores.extend(uis)

    return scores


class UserActivityConstructScore(db.Model):
    """
    A user's construct score for an activity at a specific time
    """
    __tablename__ = "user_activity_construct_score"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    activity_id = db.Column(
        db.Integer,
        db.ForeignKey("activity.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    construct_id = db.Column(
        db.Integer,
        db.ForeignKey("construct.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)

    @staticmethod
    def get_latest_scores(user_ids, activity_ids, construct_ids):
        subq = UserScore.query(
            UserScore.user_id,
            UserScore.activity_id,
            UserScore.construct_id,
            func.max(UserScore.timestamp).label('maxdate')
        ).group_by(
            UserScore.user_id,
            UserScore.activity_id,
            UserScore.construct_id).subquery('t2')

        query = UserScore.query.join(
            subq,
            and_(
                UserScore.user_id == subq.c.user_id,
                UserScore.activity_id == subq.c.activity_id,
                UserScore.construct_id == subq.c.construct_id,
                UserScore.timestamp == subq.c.maxdate
            )
        )

        return query.all()


class UserConstructScore(db.Model):
    """
    A user's construct score for the course at a specific time
    """
    __tablename__ = "user_construct_score"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    construct_id = db.Column(
        db.Integer,
        db.ForeignKey("construct.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)
    construct = db.relationship("Construct")
    activity_id = None


class CollectionActivityConstructScore(db.Model):
    """
    Collections can be used for groups of users. The collection score is analogous to the user score except that the
    score is the sum of the user scores for all user with role `member` for the given collection.
    """
    __tablename__ = "collection_activity_construct_score"

    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collection.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    activity_id = db.Column(
        db.Integer,
        db.ForeignKey("activity.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=True)
    construct_id = db.Column(
        db.Integer,
        db.ForeignKey("construct.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)


class CollectionConstructScore(db.Model):
    """
    Collections can be used for groups of users. The collection score is analogous to the user score except that the
    score is the sum of the user scores for all user with role `member` for the given collection.
    """
    __tablename__ = "collection_construct_score"

    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collection.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    construct_id = db.Column(
        db.Integer,
        db.ForeignKey("construct.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)
    activity_id = None


class UserScore(db.Model):
    """
    A user's score for a course
    """
    __tablename__ = "user_score"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collection.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    construct_id = None
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)
    activity_id = None

    @staticmethod
    def get_latest_scores(collection_id):
        subq = db.session.query(
            UserScore.user_id,
            UserScore.collection_id,
            func.max(UserScore.timestamp).label('maxdate')
        ).filter(UserScore.collection_id == collection_id).group_by(
            UserScore.user_id,
            UserScore.collection_id).subquery('t2')

        query = UserScore.query.join(
            subq,
            and_(
                UserScore.user_id == subq.c.user_id,
                UserScore.collection_id == subq.c.collection_id,
                UserScore.timestamp == subq.c.maxdate
            )
        )

        return query.all()


class CollectionActivityScore(db.Model):
    """
    Collections can be used for groups of users. The collection score is analogous to the user score except that the
    score is the sum of the user scores for all user with role `member` for the given collection.
    """
    __tablename__ = "collection_activity_score"

    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collection.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    activity_id = db.Column(
        db.Integer,
        db.ForeignKey("activity.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=True)
    construct_id = None
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)


class CollectionScore(db.Model):
    """
    Collections can be used for groups of users. The collection score is analogous to the user score except that the
    score is the sum of the user scores for all user with role `member` for the given collection.
    """
    __tablename__ = "collection_score"

    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collection.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    construct_id = None
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)
    activity_id = None
