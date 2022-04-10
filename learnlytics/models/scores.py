"""
This module contains the model for construct scores
"""

import csv
import io
from sqlalchemy import or_, desc

from learnlytics.authorization.manager import authorize
from learnlytics.database.authorization.collection import Collection
import learnlytics.database.studydata as md


class ScoresModel(object):  # pylint: disable=no-init
    """
    Contains a methods which get scores
    """

    @staticmethod
    def get_construct_scores(
            collection_id, collection_ids, construct_ids, user_ids, activity_ids, start_time, end_time,
            out_format="json"):
        """
        Gets the construct scores for the given info
        """
        collection = Collection.get(collection_id, required=True)
        res = []

        if user_ids == "all":
            user_ids = collection.all_user_ids

        if activity_ids == "all":
            activity_ids = []
            for activity in collection.activities:
                if authorize(activity.collection, ["see_invisible_activities"], do_abort=False) or \
                        activity.visibility == "T":
                    activity_ids.append(activity.id)

        if construct_ids == "all":
            construct_ids = []
            for model in collection.construct_models:
                for construct in model.constructs:
                    construct_ids.append(construct.id)

        if activity_ids is None:
            scores = md.UserConstructScore.query.\
                filter(md.UserConstructScore.construct_id.in_(construct_ids)).\
                filter(md.UserConstructScore.user_id.in_(user_ids)).\
                order_by(desc(md.UserConstructScore.timestamp)).all()

            scores.extend(
                md.CollectionConstructScore.query.
                filter(md.CollectionConstructScore.construct_id.in_(construct_ids)).
                filter(md.CollectionConstructScore.collection_id.in_(collection_ids)).
                order_by(desc(md.CollectionConstructScore.timestamp)).all())
        else:
            scores = md.UserActivityConstructScore.query.\
                filter(md.UserActivityConstructScore.activity_id.in_(activity_ids)).\
                filter(md.UserActivityConstructScore.construct_id.in_(construct_ids)).\
                filter(md.UserActivityConstructScore.user_id.in_(user_ids)).\
                order_by(desc(md.UserActivityConstructScore.timestamp)).all()

            scores.extend(
                md.CollectionActivityConstructScore.query.
                filter(md.CollectionActivityConstructScore.activity_id.in_(activity_ids)).
                filter(md.CollectionActivityConstructScore.construct_id.in_(construct_ids)).
                filter(md.CollectionActivityConstructScore.collection_id.in_(collection_ids)).
                order_by(desc(md.CollectionActivityConstructScore.timestamp)).all())

        if out_format == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['construct_id', 'score', 'timestamp', 'user_id', 'collection_id', 'activity_id']
            writer.writerow(line)

        for score in scores:
            if score.max_score == 0:
                scaled_score = 0
            else:
                scaled_score = score.score / score.max_score

            if out_format == "json":
                score_dict = {
                    "construct_id": score.construct_id,
                    "score": scaled_score,
                    "timestamp": score.timestamp
                }
                if hasattr(score, "user_id"):
                    score_dict["user_id"] = score.user_id
                if hasattr(score, "collection_id"):
                    score_dict["collection_id"] = score.collection_id
                if score.activity_id is not None:
                    score_dict["activity_id"] = score.activity_id
                res.append(score_dict)
            elif out_format == "csv":
                row = [
                    str(score.construct_id),
                    str(scaled_score),
                    str(score.timestamp)
                ]
                if hasattr(score, "user_id"):
                    row.append(str(score.user_id))
                if hasattr(score, "collection_id"):
                    row.append(str(score.collection_id))
                if score.activity_id is not None:
                    row.append(str(score.activity_id))
                writer.writerow(row)
        if out_format == "json":
            return res
        elif out_format == "csv":
            output.seek(0)
            return output

    @staticmethod
    def get_scores(collection_id, collection_ids, user_ids, activity_ids, start_time, end_time, out_format="json"):
        """
        Gets the scores for the given info
        """
        collection = Collection.get(collection_id, required=True)
        res = []

        if user_ids == "all":
            user_ids = collection.all_user_ids

        if activity_ids == "all":
            activity_ids = []
            for activity in collection.activities:
                if authorize(activity.collection, ["see_invisible_activities"], do_abort=False) or \
                        activity.visibility == "T":
                    activity_ids.append(activity.id)

        if activity_ids is None:
            scores = md.UserScore.query.\
                filter(md.UserScore.user_id.in_(user_ids)).\
                order_by(desc(md.UserScore.timestamp)).all()

            scores.extend(
                md.CollectionScore.query.
                filter(md.CollectionScore.collection_id.in_(collection_ids)).
                order_by(desc(md.CollectionScore.timestamp)).all())
        else:
            scores = []

            scores.extend(
                md.CollectionActivityScore.query.
                filter(md.CollectionActivityScore.activity_id.in_(activity_ids)).
                filter(md.CollectionActivityScore.collection_id.in_(collection_ids)).
                order_by(desc(md.CollectionActivityScore.timestamp)).all())

        for score in scores:
            if score.max_score == 0:
                scaled_score = 0
            else:
                scaled_score = score.score / score.max_score

            score_dict = {
                "score": scaled_score,
                "timestamp": score.timestamp
            }
            if hasattr(score, "user_id"):
                score_dict["user_id"] = score.user_id
            if hasattr(score, "collection_id"):
                score_dict["collection_id"] = score.collection_id
            if score.activity_id is not None:
                score_dict["activity_id"] = score.activity_id
            res.append(score_dict)

        return res
