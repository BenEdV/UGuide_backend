from datetime import datetime

from learnlytics.extensions import db
from learnlytics.database.construct.construct import Construct, ConstructActivity, ConstructActivityRelationType
import learnlytics.database.studydata as md
from learnlytics.models.construct_models.base_construct_model import BaseConstructModel


class ThermosModel(BaseConstructModel):
    supported_activities = ["survey", "question.likert"]
    supported_activity_relation_types = ["exam_question"]
    supported_construct_types = ["positive_trait", "negative_trait"]
    supported_construct_relation_types = ["taxonomical"]
    supported_construct_activity_relation_types = ["exhibits"]
    method = "thermos_model"

    def __init__(self, model_id):
        from learnlytics.database.construct.construct import ConstructModel
        self.model = ConstructModel.get(model_id)

        self.get_scores = {
            "survey": {
                "exhibits": self.__scores_for_survey
            },
            "question.likert": {
                "exhibits": self.__scores_for_question_likert
            }
        }

    def create_model(name, parameters):
        from learnlytics.database.construct.construct import ConstructModel
        model = ConstructModel(name=name, method=ThermosModel.method, parameters=parameters)

        return model

    def add_new_results(self, data, activity_ids, user_ids):
        """
        :param data: Array of tuples containing (activity_id, user_id, statement)
        """
        query = db.session.query(
            ConstructActivity.activity_id,
            ConstructActivity.properties,
            ConstructActivity.construct_id,
            ConstructActivityRelationType.name,
            md.ActivityType.name
        ).\
            filter(ConstructActivity.activity_id.in_(activity_ids)).\
            join(ConstructActivityRelationType).\
            filter(ConstructActivityRelationType.name.in_(self.supported_construct_activity_relation_types)).\
            join(Construct).\
            filter(Construct.model_id == self.model.id).\
            join(md.Activity).\
            join(md.ActivityType)

        construct_activities = query.all()

        constructs_for_activity = {}
        construct_ids = []
        for (activity_id, properties, construct_id, relation_type, activity_type) in construct_activities:
            if activity_id not in constructs_for_activity:
                constructs_for_activity[activity_id] = []
            constructs_for_activity[activity_id].append((construct_id, properties, relation_type, activity_type))
            construct_ids.append(construct_id)

        user_scores = md.get_scores(
            self.model.collection.member_ids,
            self.model.construct_ids,
            self.model.collection.activity_ids)

        ucs_dict = {}  # user construct score
        for user_score in user_scores:
            self.__add_score_to_uc_dict(ucs_dict, user_score)

        activity_relations = md.ActivityRelation.query.\
            join(md.ActivityRelationType).\
            filter(md.ActivityRelationType.name.in_(self.supported_activity_relation_types)).\
            filter(md.ActivityRelation.head_activity_id.in_(activity_ids)).all()
        exam_for_question = {}
        for activity_relation in activity_relations:
            if activity_relation.type.name == "exam_question":
                exam_for_question[activity_relation.head_activity_id] = activity_relation.tail_activity_id

        for (activity_id, user_id, statement) in data:
            if user_id is None:
                continue

            for construct_id, properties, relation_type, activity_type in constructs_for_activity.get(activity_id, []):
                score, max_score = self.get_scores[activity_type][relation_type](statement["result"], properties)
                timestamp = datetime.fromisoformat(statement["timestamp"].replace("Z", "+00:00"))

                if self.__exists_score_in_uc_dict(ucs_dict, activity_id, user_id, construct_id, timestamp):
                    # This statement has already been handled
                    continue

                related_activity_ids = [activity_id, None]
                if activity_id in exam_for_question:
                    related_activity_ids.append(exam_for_question[activity_id])

                construct = Construct.get(construct_id, required=True)
                for construct_id in self.__get_construct_ancestor_ids(construct):
                    for related_activity_id in related_activity_ids:
                        if related_activity_id is not None and construct_id is None:
                            continue
                        if self.__exists_score_in_uc_dict(
                                ucs_dict, related_activity_id, user_id, construct_id, timestamp):
                            ucs = ucs_dict[related_activity_id][construct_id][timestamp][user_id]
                        else:
                            ucs = md.new_construct_score(
                                user_id=user_id,
                                collection_id=self.model.collection_id,
                                activity_id=related_activity_id,
                                construct_id=construct_id,
                                timestamp=timestamp
                            )
                            if statement["verb"]["id"] == "http://adlnet.gov/expapi/verbs/initialized":
                                ucs.score = 0
                                ucs.max_score = 0
                            db.session.add(ucs)
                            self.__add_score_to_uc_dict(ucs_dict, ucs)
                        ucs.score += score
                        ucs.max_score += max_score

        db.session.commit()

    def __add_score_to_uc_dict(self, score_dict, score):
        if score.activity_id not in score_dict:
            score_dict[score.activity_id] = {}
        if score.construct_id not in score_dict[score.activity_id]:
            score_dict[score.activity_id][score.construct_id] = {}
        if score.timestamp not in score_dict[score.activity_id][score.construct_id]:
            score_dict[score.activity_id][score.construct_id][score.timestamp] = {}
        if score.user_id not in score_dict[score.activity_id][score.construct_id][score.timestamp]:
            score_dict[score.activity_id][score.construct_id][score.timestamp][score.user_id] = score

    def __exists_score_in_uc_dict(self, score_dict, activity_id, user_id, construct_id, timestamp):
        if activity_id not in score_dict:
            return False
        if construct_id not in score_dict[activity_id]:
            return False
        if timestamp not in score_dict[activity_id][construct_id]:
            return False
        if user_id not in score_dict[activity_id][construct_id][timestamp]:
            return False
        return True

    def __get_construct_ancestor_ids(self, construct):
        ancestors = [construct.id]
        while(True):
            if construct.tail_constructs == []:
                break
            construct = construct.tail_constructs[0]
            ancestors.append(construct.id)

        return ancestors

    # question score determination methods
    def __scores_for_survey(self, result, properties):

        score = 0
        max_score = 0

        return score, max_score

    def __scores_for_question_likert(self, result, properties):

        score = int(result["response"]) + 1

        max_score = 7

        return score, max_score
