import json
import logging

from collections import deque
from flask import abort
from sqlalchemy.sql import func
from sqlalchemy import and_

from learnlytics.authentication import current_identity
from learnlytics.extensions import db
import learnlytics.database.studydata as md


logger = logging.getLogger(__name__)


class SpinData(object):
    """
    The class containing the methods to get data from the LRS, and put in into spindata
    """

    def get_users_exams_concept_scores(self, exam_ids, user_ids=None, parent_id=None, misconcepts=False):
        # pylint: disable=too-many-locals
        """
        Get the concept scores for given list of users
        :param exam_ids: The exams to use
        :param user_ids: The users to use
        :param parent_id: The Id of the concept which childs need to be calculated, -1 for top level
        :param misconcepts: Determines if misconcepts or non-misconcepts need to be returned
        :return: The total concept scores for given exams and students
        """

        concepts = md.Concept.query.\
            filter(and_(md.Concept.is_misconcept == misconcepts, md.Concept.parent_concept_id == parent_id)).all()

        if user_ids is None:
            user = current_identity()
            user_ids = [user.id]

        # Results dic
        concept_score_dict = {}

        for concept in concepts:
            concept_score_dict[concept.id] = {
                "id": concept.id,
                "name": concept.name,
                "parent_id": concept.parent_concept_id,
                "weight": concept.weight,
                "is_misconcept": concept.is_misconcept,
                "score": 0,
                "is_leaf": concept.is_leaf,
                "description": concept.description}
            (uec_score, uec_max_score) = db.session.query(
                func.sum(md.UserExamConceptScore.score),
                func.sum(md.UserExamConceptScore.max_score)).filter(
                md.UserExamConceptScore.concept_id == concept.id,
                md.UserExamConceptScore.user_id.in_(user_ids),
                md.UserExamConceptScore.exam_id.in_(exam_ids)).one()
            if uec_max_score and uec_max_score > 0:
                concept_score_dict[concept.id]["score"] = uec_score / uec_max_score * 100
            else:
                concept_score_dict[concept.id]["score"] = 0

        return concept_score_dict


def format_spin_data(data):
    names = []
    weights = []
    parent_ids = []
    scores = [[]]
    is_misconcepts = []
    ids = []
    is_leafs = []
    descriptions = []
    for field in data.values():
        names.append(field["name"])
        weights.append(field["weight"])
        parent_ids.append(field["parent_id"])
        scores[0].append(round(field["score"], 3))
        is_misconcepts.append(field["is_misconcept"])
        ids.append(field["id"])
        is_leafs.append(field["is_leaf"])
        descriptions.append(field["description"])

    return {
        "names": names,
        "weights": weights,
        "parent_ids": parent_ids,
        "scores": scores,
        "is_misconcepts": is_misconcepts,
        "ids": ids,
        "is_leafs": is_leafs,
        "descriptions": descriptions
    }


def add_scores(formatted_data, data):
    scores = []
    for field in data:
        scores.append(round(field["score"], 3))

    formatted_data["scores"].append(scores)
    return formatted_data
