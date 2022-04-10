# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course (3 4)
# (C) Copyright Utrecht University (Department of Information and Computing Sciences)
import copy
from datetime import datetime

from learnlytics.extensions import db
from learnlytics.database.authorization.collection import UserCollectionSettings
from learnlytics.database.authorization.role import Role
from learnlytics.database.authorization.user import UserRole
from learnlytics.database.construct.construct import Construct, ConstructActivity, ConstructActivityRelationType
import learnlytics.database.studydata as md
from learnlytics.models.construct_models.base_construct_model import BaseConstructModel


class MeanModel(BaseConstructModel):
    supported_activities = ["exam", "question.multiple_choice", "question.multiple_selection", "question.open"]
    supported_activity_relation_types = ["exam_question"]
    supported_construct_types = ["concept", "misconception"]
    supported_construct_relation_types = ["taxonomical"]
    supported_construct_activity_relation_types = ["tests", "exhibits"]
    method = "mean_model"

    def __init__(self, model_id):
        from learnlytics.database.construct.construct import ConstructModel
        self.model = ConstructModel.get(model_id)

        self.get_scores = {
            "tests": {
                "question.multiple_choice": self.__scores_for_multiple_choice_concept,
                "question.multiple_selection": self.__scores_for_multiple_selection_concept,
                "question.open": self.__scores_for_open_concept
            },
            "exhibits": {
                "question.multiple_choice": self.__scores_for_multiple_choice_misconception,
                "question.multiple_selection": self.__scores_for_multiple_selection_misconception,
                "question.open": self.__scores_for_open_misconception
            }
        }

    def create_model(name, parameters):
        from learnlytics.database.construct.construct import ConstructModel
        model = ConstructModel(name=name, method=MeanModel.method, parameters=parameters)

        return model

    def init_empty_activity_scores(self, construct_id, activity_ids):
        """
        Checks if there are existing scores for the questions and their exams. Initialize with score, max_score = 0, 0
        if not present.
        """
        scores = []
        collection = self.model.collection
        start_time = collection.course_instance.period.start_date

        for activity_id in activity_ids:
            for member in collection.members:
                score = md.UserScore(
                    user_id=member.id,
                    activity_id=None,
                    construct_id=construct_id,
                    timestamp=start_time,
                    score=0,
                    max_score=0)
                scores.append(score)

            for sub_collection in collection.children:
                score = md.CollectionScore(
                    collection_id=sub_collection.id,
                    activity_id=activity_id,
                    construct_id=construct_id,
                    timestamp=start_time,
                    score=0,
                    max_score=0)
                scores.append(score)

        db.session.add_all(scores)

    def init_new_construct_scores(self, construct_id, course_id):
        """
        After a new construct has been created it's global score for all users and groups must be initialized
        """
        scores = []
        course = md.Course.get(course_id, required=True)

        for user_id in course.user_ids:
            score = md.UserConceptScore(
                user_id=user_id,
                concept_id=construct_id,
                score=0,
                max_score=0)
            scores.append(score)

        for group_id in course.group_ids:
            score = md.GroupConceptScore(
                group_id=group_id,
                concept_id=construct_id,
                score=0,
                max_score=0)
            scores.append(score)

        db.session.add_all(scores)

    def remove_empty_scores(self, construct_id, question_ids):
        for question_id in question_ids:
            question = md.Activity.get(question_id, required=True)

            md.UserActivityConceptScore.query.filter(
                md.UserActivityConceptScore.concept_id == construct_id,
                md.UserActivityConceptScore.question_id == question_id).delete()
            md.GroupActivityConceptScore.query.filter(
                md.GroupActivityConceptScore.concept_id == construct_id,
                md.GroupActivityConceptScore.question_id == question_id).delete()

            md.UserExamConceptScore.query.filter(
                md.UserExamConceptScore.concept_id == construct_id,
                md.UserExamConceptScore.exam_id == question.exam_id,
                md.UserExamConceptScore.max_score == 0).delete()
            md.GroupExamConceptScore.query.filter(
                md.GroupExamConceptScore.concept_id == construct_id,
                md.GroupExamConceptScore.exam_id == question.exam_id,
                md.GroupExamConceptScore.max_score == 0).delete()

        construct = md.Concept.get(construct_id, required=True)
        if construct.parent_concept_id is not None:
            self.remove_empty_scores(construct.parent_concept_id, question_ids)

    def new_group():
        pass

    def change_group():
        pass

    def delete_group():
        pass

    def change_construct_parent(self, construct_id, old_parent_id, new_parent_id, old_weight, new_weight):
        construct_ids = [construct_id]

        if old_parent_id:
            old_parent = md.Concept.get(old_parent_id)
            old_ancestor_ids = [(old_parent_id, old_weight)]
            construct_ids.append(old_parent_id)

            while old_parent.parent_concept_id:
                construct_ids.append(old_parent.parent_concept_id)
                old_ancestor_ids.append((old_parent.parent_concept_id, old_parent.weight))
                old_parent = old_parent.parent
        else:
            old_ancestor_ids = []

        if new_parent_id:
            new_parent = md.Concept.get(new_parent_id)
            new_ancestor_ids = [(new_parent_id, new_weight)]
            construct_ids.append(new_parent_id)

            while new_parent.parent_concept_id:
                construct_ids.append(new_parent.parent_concept_id)
                new_ancestor_ids.append((new_parent.parent_concept_id, new_parent.weight))
                new_parent = new_parent.parent
        else:
            new_ancestor_ids = []

        scores = dict()
        for uqc_score in md.UserActivityConceptScore.query.filter(
                md.UserActivityConceptScore.concept_id.in_(construct_ids)).all():
            key = "uq" + str(uqc_score.user_id) + " " + str(uqc_score.question_id)
            if key in scores:
                scores[key][uqc_score.concept_id] = uqc_score
            else:
                scores[key] = {uqc_score.concept_id: uqc_score}

        for uec_score in md.UserExamConceptScore.query.filter(
                md.UserExamConceptScore.concept_id.in_(construct_ids)).all():
            key = "ue" + str(uec_score.user_id) + " " + str(uec_score.exam_id)
            if key in scores:
                scores[key][uec_score.concept_id] = uec_score
            else:
                scores[key] = {uec_score.concept_id: uec_score}

        for uc_score in md.UserConceptScore.query.filter(
                md.UserConceptScore.concept_id.in_(construct_ids)).all():
            key = "uc" + str(uc_score.user_id)
            if key in scores:
                scores[key][uc_score.concept_id] = uc_score
            else:
                scores[key] = {uc_score.concept_id: uc_score}

        for gqc_score in md.GroupActivityConceptScore.query.filter(
                md.GroupActivityConceptScore.concept_id.in_(construct_ids)).all():
            key = "gq" + str(gqc_score.group_id) + " " + str(gqc_score.question_id)
            if key in scores:
                scores[key][gqc_score.concept_id] = gqc_score
            else:
                scores[key] = {gqc_score.concept_id: gqc_score}

        for gec_score in md.GroupExamConceptScore.query.filter(
                md.GroupExamConceptScore.concept_id.in_(construct_ids)).all():
            key = "ge" + str(gec_score.group_id) + " " + str(gec_score.exam_id)
            if key in scores:
                scores[key][gec_score.concept_id] = gec_score
            else:
                scores[key] = {gec_score.concept_id: gec_score}

        for gc_score in md.GroupConceptScore.query.filter(
                md.GroupConceptScore.concept_id.in_(construct_ids)).all():
            key = "gc" + str(gc_score.group_id)
            if key in scores:
                scores[key][gc_score.concept_id] = gc_score
            else:
                scores[key] = {gc_score.concept_id: gc_score}

        for (key, score_set) in scores.items():
            if construct_id not in score_set:
                continue

            weight = 1
            for (old_ancestor_id, w) in old_ancestor_ids:
                weight *= w
                if old_ancestor_id not in score_set:
                    score_set[old_ancestor_id] = self.__create_missing_score(key, old_ancestor_id)
                    db.session.add(score_set[old_ancestor_id])
                score_set[old_ancestor_id].score -= score_set[construct_id].score * weight
                score_set[old_ancestor_id].max_score -= score_set[construct_id].max_score * weight
            weight = 1
            for (new_ancestor_id, w) in new_ancestor_ids:
                weight *= w
                if new_ancestor_id not in score_set:
                    score_set[new_ancestor_id] = self.__create_missing_score(key, new_ancestor_id)
                    db.session.add(score_set[new_ancestor_id])

                score_set[new_ancestor_id].score += score_set[construct_id].score * weight
                score_set[new_ancestor_id].max_score += score_set[construct_id].max_score * weight

    def __create_missing_score(self, key, construct_id):
        score_type = key[:2]
        ids = key[2:].split(" ")

        if score_type == "uq":
            return md.UserActivityConceptScore(
                user_id=ids[0],
                question_id=ids[1],
                concept_id=construct_id,
                score=0,
                max_score=0)
        if score_type == "ue":
            return md.UserExamConceptScore(
                user_id=ids[0],
                exam_id=ids[1],
                concept_id=construct_id,
                score=0,
                max_score=0)
        if score_type == "uc":
            return md.UserConceptScore(
                user_id=ids[0],
                concept_id=construct_id,
                score=0,
                max_score=0)
        if score_type == "gq":
            return md.GroupActivityConceptScore(
                group_id=ids[0],
                question_id=ids[1],
                concept_id=construct_id,
                score=0,
                max_score=0)
        if score_type == "ge":
            return md.GroupExamConceptScore(
                group_id=ids[0],
                exam_id=ids[1],
                concept_id=construct_id,
                score=0,
                max_score=0)
        if score_type == "gc":
            return md.GroupConceptScore(
                group_id=ids[0],
                concept_id=construct_id,
                score=0,
                max_score=0)

    def change_mapping(self, construct_id, changes, user_ids=None):
        """
        expects
        {
            question_id1: {
                answer_id1: {
                    old_weight: 1.
                    new_weight: 0
                },
                answer_id2: {
                    old_weight: 0.
                    new_weight: 1
                }
            }
        }
        """
        for question_id, answer_ids in changes.items():
            if user_ids is None:
                user_ids = []
                for (user_id, ) in db.session.query(md.User.id).\
                        join(md.Person, md.User.id == md.Person.user_id).\
                        join(md.ExamResult, md.Person.id == md.ExamResult.person_id).\
                        join(md.ActivityResult, md.ExamResult.id == md.ActivityResult.exam_result_id).\
                        filter(md.ActivityResult.question_id == question_id).\
                        all():
                    user_ids.append(user_id)

            question = md.Activity.get(question_id, required=True)
            construct = md.Concept.get(construct_id, required=True)

            max_diff = self.update_max_question_types[question.type](answer_ids)

            user_groups = dict()
            group_sizes = dict()
            for (user_id, group_id) in db.session.query(md.User.id, md.Group.id).\
                    join(md.Group, md.User.groups).\
                    filter(md.Group.course_id == question.exam.course_id, md.User.id.in_(user_ids)).all():
                # TODO course_id from model
                if group_id in group_sizes:
                    group_sizes[group_id] += 1
                else:
                    group_sizes[group_id] = 1
                if user_id in user_groups:
                    user_groups[user_id].append(group_id)
                else:
                    user_groups[user_id] = [group_id]

            user_scores = dict()
            for uqc_score in md.UserActivityConceptScore.query.filter(
                    md.UserActivityConceptScore.concept_id == construct_id,
                    md.UserActivityConceptScore.user_id.in_(user_ids),
                    md.UserActivityConceptScore.question_id == question_id).all():
                user_scores[uqc_score.user_id] = [uqc_score]
                uqc_score.max_score += max_diff

            for uec_score in md.UserExamConceptScore.query.filter(
                    md.UserExamConceptScore.concept_id == construct_id,
                    md.UserExamConceptScore.user_id.in_(user_ids),
                    md.UserExamConceptScore.exam_id == question.exam_id).all():
                user_scores[uec_score.user_id].append(uec_score)
                uec_score.max_score += max_diff

            for uc_score in md.UserConceptScore.query.filter(
                    md.UserConceptScore.user_id.in_(user_ids),
                    md.UserConceptScore.concept_id == construct_id).all():
                user_scores[uc_score.user_id].append(uc_score)
                uc_score.max_score += max_diff

            group_scores = dict()
            for gqc_score in md.GroupActivityConceptScore.query.filter(
                    md.GroupActivityConceptScore.concept_id == construct_id,
                    md.GroupActivityConceptScore.question_id == question_id).all():
                if gqc_score.group_id not in group_sizes:
                    continue
                group_scores[gqc_score.group_id] = [gqc_score]
                gqc_score.max_score += max_diff * group_sizes[gqc_score.group_id]

            for gec_score in md.GroupExamConceptScore.query.filter(
                    md.GroupExamConceptScore.concept_id == construct_id,
                    md.GroupExamConceptScore.exam_id == question.exam_id).all():
                if gec_score.group_id not in group_sizes:
                    continue
                group_scores[gec_score.group_id].append(gec_score)
                gec_score.max_score += max_diff * group_sizes[gec_score.group_id]

            for gc_score in md.GroupConceptScore.query.filter(
                    md.GroupConceptScore.concept_id == construct_id).all():
                if gc_score.group_id not in group_sizes:
                    continue
                group_scores[gc_score.group_id].append(gc_score)
                gc_score.max_score += max_diff * group_sizes[gc_score.group_id]

            uqc_diffs = self.update_question_types[question.type](question_id, answer_ids)

            for (user_id, diff) in uqc_diffs.items():
                for user_score in user_scores[user_id]:
                    user_score.score += diff

                for group_id in user_groups[user_id]:
                    for group_score in group_scores[group_id]:
                        group_score.score += diff

        if construct.parent_concept_id is None:
            return

        for question_id, answer_ids in changes.items():
            for answer_id in answer_ids:
                changes[question_id][answer_id]["old_weight"] *= construct.weight
                changes[question_id][answer_id]["new_weight"] *= construct.weight

        self.change_mapping(construct.parent_concept_id, changes)

    def add_new_results(self, data, activity_ids, user_ids):
        """
        :param data: Array of tuples containing (activity_id, user_id, statement)
        """
        query = db.session.query(
            ConstructActivity.activity_id,
            ConstructActivity.properties,
            ConstructActivity.construct_id,
            ConstructActivityRelationType.name
        ).\
            filter(ConstructActivity.activity_id.in_(activity_ids)).\
            join(ConstructActivityRelationType).\
            filter(ConstructActivityRelationType.name.in_(self.supported_construct_activity_relation_types)).\
            join(Construct).\
            filter(Construct.model_id == self.model.id)

        construct_activities = query.all()

        constructs_for_activity = {}
        construct_ids = []
        for (activity_id, properties, construct_id, relation_type) in construct_activities:
            if activity_id not in constructs_for_activity:
                constructs_for_activity[activity_id] = []
            constructs_for_activity[activity_id].append((construct_id, properties, relation_type))
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

        type_for_activity = {}
        activities = md.Activity.query.filter(md.Activity.id.in_(activity_ids)).all()
        for activity in activities:
            type_for_activity[activity.id] = activity.type.name

        for (activity_id, user_id, statement) in data:
            if user_id is None:
                continue

            for (construct_id, properties, relation_type) in constructs_for_activity.get(activity_id, []):
                score, max_score = self.get_scores[relation_type][type_for_activity[activity_id]](
                    statement["result"],
                    properties)
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
                            db.session.add(ucs)
                            self.__add_score_to_uc_dict(ucs_dict, ucs)
                        ucs.score += score
                        ucs.max_score += max_score

        self.__update_dynamic_groups()
        self.__update_collection_scores(ucs_dict)
        self.__shift_social_comparison()
        db.session.commit()

    def __update_dynamic_groups(self):
        upper = None
        lower = None
        for child in self.model.collection.children:
            if child.name == "upper_50":
                upper = child
            if child.name == "lower_50":
                lower = child

        if upper is None or lower is None:
            print("No social comparison")
            return

        member_role = Role.get_name("member")
        UserRole.query.filter(UserRole.role_id == member_role.id, UserRole.collection_id == upper.id).delete()
        UserRole.query.filter(UserRole.role_id == member_role.id, UserRole.collection_id == lower.id).delete()

        scores = md.UserScore.get_latest_scores(self.model.collection_id)
        scores = sorted(scores, key=lambda score: score.score)

        lower_scores = scores[:len(scores) // 2]
        upper_scores = scores[len(scores) // 2:]

        for score in lower_scores:
            member = UserRole(collection_id=lower.id, role_id=member_role.id, user_id=score.user_id)
            db.session.add(member)

        for score in upper_scores:
            member = UserRole(collection_id=upper.id, role_id=member_role.id, user_id=score.user_id)
            db.session.add(member)

    def __update_collection_scores(self, score_dict):
        collections = [self.model.collection]
        collection_ids = [self.model.collection_id]
        for child in self.model.collection.children:
            collections.append(child)
            collection_ids.append(child.id)

        # delete existing collection scores
        md.CollectionScore.query.filter(
            md.CollectionScore.collection_id.in_(collection_ids)).delete(synchronize_session=False)
        md.CollectionConstructScore.query.filter(
            md.CollectionConstructScore.collection_id.in_(collection_ids)).delete(synchronize_session=False)
        md.CollectionActivityConstructScore.query.filter(
            md.CollectionActivityConstructScore.collection_id.in_(collection_ids)).delete(synchronize_session=False)

        for collection in collections:
            member_ids = collection.member_ids

            for activity_id, dic in score_dict.items():
                for construct_id, dic in dic.items():
                    sc = {}
                    window_scores = {}
                    prev_date = None
                    for timestamp, dic in sorted(dic.items()):
                        if prev_date is not None and prev_date != timestamp.date():
                            sc[prev_date] = copy.deepcopy(window_scores)
                        prev_date = timestamp.date()

                        for user_id, score in dic.items():
                            if user_id in member_ids:
                                window_scores[user_id] = score

                    sc[prev_date] = copy.deepcopy(window_scores)
                    for date, scores in sc.items():
                        sum_score = sum(score.score for score in scores.values())
                        sum_max_score = sum(score.max_score for score in scores.values())

                        score = md.new_collection_construct_score(
                            collection_id=collection.id,
                            construct_id=construct_id,
                            timestamp=date,
                            activity_id=activity_id,
                            score=sum_score,
                            max_score=sum_max_score)

                        db.session.add(score)

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
        if construct.type.name == "misconception":
            return [construct.id]
        ancestors = [None, construct.id]
        while(True):
            if construct.tail_constructs == []:
                break
            construct = construct.tail_constructs[0]
            ancestors.append(construct.id)

        return ancestors

    def __shift_social_comparison(self):
        settings = UserCollectionSettings.query.\
            filter(UserCollectionSettings.collection_id == self.model.collection_id).all()
        ids = [self.model.collection_id]
        for child in self.model.collection.children:
            ids.append(child.id)
        cycle = {}
        for index in range(0, len(ids)):
            cycle[ids[index]] = ids[(index + 1) % len(ids)]

        for setting in settings:
            # copy hack to make SQLAlchemy ORM persist changes
            old_settings = setting.settings.copy()
            if "comparison_collection_id" in old_settings:
              old_settings["comparison_collection_id"] = cycle[old_settings["comparison_collection_id"]]
            setting.settings = old_settings

    # question score determination methods

    def __scores_for_multiple_choice_concept(self, result, properties):
        if result["response"] in properties["value_pairs"]:
            score = properties["value_pairs"][result["response"]]
        else:
            score = 0

        max_score = max(properties["value_pairs"].values())

        return score, max_score

    def __scores_for_multiple_choice_misconception(self, result, properties):
        if result["response"] in properties["value_pairs"]:
            score = properties["value_pairs"][result["response"]]
        else:
            score = 0

        max_score = max(properties["value_pairs"].values())

        return score, max_score

    def __scores_for_multiple_selection_concept(self, result, properties):
        score = 0
        for response in result["response"].split(','):
            if response in properties["value_pairs"]:
                score += properties["value_pairs"][response]

        max_score = sum(properties["value_pairs"].values())

        return score, max_score

    def __scores_for_multiple_selection_misconception(self, result, properties):
        score = 0
        for response in result["response"].split(','):
            if response in properties["value_pairs"]:
                score += properties["value_pairs"][response]

        max_score = sum(properties["value_pairs"].values())

        return score, max_score

    def __scores_for_open_concept(self, result, properties):
        if result["success"]:
            score = 1
        else:
            score = 0

        max_score = 1

        return score, max_score

    def __scores_for_open_misconception(self, result, properties):
        if not result["success"]:
            score = properties["value_pairs"][""]
        else:
            score = 0

        max_score = properties["value_pairs"][""]

        return score, max_score
