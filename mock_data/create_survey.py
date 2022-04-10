#!/usr/bin/env python3

# pylint: skip-file

import os
import sys
sys.path.append(os.getcwd())

from config import get_config
from sqlalchemy.orm.attributes import flag_modified

from learnlytics.app import create_minimal_app
from learnlytics.extensions import db
from learnlytics.database.construct import Construct, ConstructModel, ConstructType, \
  ConstructActivity, ConstructActivityRelationType, ConstructRelation, ConstructRelationType
from learnlytics.database.studydata.activity import Activity, ActivityType, ActivityRelationType, ActivityRelation
from learnlytics.database.authorization.collection import Collection
from mock_data.survey_data import all_exercises, thermos_construct_types, thermos_models_and_constructs, \
  thermos_questions, thermos_comments, thermos_feedback_questions

class MockSurvey():
    def __init__(self, db):
        self.db = db

    def create_survey(self):
        collection_name = "Universiteit"
        collection_id = Collection.get_name(collection_name).id

        print(f"Adding Thermos models & constructs to {collection_name}...")
        models = self.add_models(
            collection_id=collection_id,
            construct_types=thermos_construct_types,
            models_and_constructs=thermos_models_and_constructs
        )

        print("Adding Thermos survey...")
        thermos_properties = {
            "retake": True,
            "see_results_before_completion": True,
            "hide_if_completed": False,
            "copyright": {
              "raw": "Survey text content is copyright © 2020 Lifelong Achievement Group"
            },
            "redirect_on_complete": ["thermos-result"]
        }
        thermos_survey = self.add_survey(
            title="Thermos",
            collection_id=collection_id,
            questions=thermos_questions,
            comments=thermos_comments,
            visibility="T",
            properties=thermos_properties
        )
        print(f"Added Survey with id: {thermos_survey.id}")

        print("Adding Thermos feedback survey...")
        feedback_properties = {
            "retake": True,
            "hide_if_completed": False,
            "redirect_on_complete": ["..", thermos_survey.id, "thermos-result"]
        }
        thermos_feedback_survey = self.add_survey(
            title="Thermos-tool Feedback",
            collection_id=collection_id,
            questions=thermos_feedback_questions,
            comments=[],
            visibility="T",
            properties=feedback_properties
        )
        thermos_survey.properties["feedback_survey_id"] = thermos_feedback_survey.id
        print(f"Added Thermos-tool Feedback Survey (with id: {thermos_feedback_survey.id})")

        print("Adding Thermos follow-up activities...")
        exercise_properties = {
            "retake": True,
            "hide_if_completed": False,
            "redirect_on_complete": ["..", thermos_survey.id, "thermos-result"],
            "copyright": {"raw": "Adapted from Motivation and Engagement Workbook UC 2016, © 2016 Copyright Lifelong Achievement Group"}
        }
        for exercises in all_exercises:
            for survey in exercises:
                exercise_survey = self.add_survey(
                    title=survey.survey_title,
                    collection_id=collection_id,
                    questions=survey.questions,
                    comments=survey.comments,
                    visibility=survey.visibility,
                    properties=exercise_properties
                )
                if survey.construct_name is not None:
                    print(f"Adding construct {survey.construct_name} to survey {survey.survey_title}")
                    construct = Construct.query.filter(Construct.name == survey.construct_name, Construct.collection_id == collection_id).one_or_none()
                    construct.properties["exercises"].append({"id": exercise_survey.id, "title": survey.survey_title, "survey_type": survey.survey_type})
                    flag_modified(construct, "properties")
                    print(construct.properties)
                print(f"Added {survey.survey_title} (with id: {exercise_survey.id})")

        print("Committing to database...")
        self.db.session.commit()

    def add_models(self, collection_id, construct_types, models_and_constructs):
        construct_types_dict = {}
        for type_name in construct_types:
            construct_type = ConstructType.query.filter(ConstructType.name == type_name).one_or_none()
            if construct_type is None:
                construct_type = ConstructType(name=type_name)
                self.db.session.add(construct_type)
                self.db.session.commit()
            construct_types_dict[type_name] = construct_type.id

        construct_relation_type = ConstructRelationType.query.filter(ConstructRelationType.name == "taxonomical").one_or_none()

        result = []
        for model_data in models_and_constructs:
            model = ConstructModel(
                name=model_data.name,
                method=model_data.method,
                collection_id=collection_id,
                description=""
            )

            self.add_constructs(constructs=model_data.constructs,
                                construct_types=construct_types_dict,
                                model=model,
                                relation_type=construct_relation_type)

            self.db.session.add(model)
            result.append(model)

        self.db.session.commit()
        return result

    def add_constructs(self, constructs, construct_types, model, relation_type, parent_construct=None):
        for construct_data in constructs:
            construct = Construct(
                name=construct_data.name,
                description="",
                type_id=construct_types[construct_data.type],
                properties=construct_data.properties
            )

            self.db.session.add(construct)
            model.constructs.append(construct)
            self.db.session.commit()

            if parent_construct is not None:
                construct_relation = ConstructRelation(
                    head_construct_id=construct.id,
                    tail_construct_id=parent_construct.id,
                    type=relation_type
                )

                self.db.session.add(construct_relation)

            if construct_data.children is not None and len(construct_data.children) > 0:
                self.add_constructs(constructs=construct_data.children,
                                    construct_types=construct_types,
                                    model=model,
                                    relation_type=relation_type,
                                    parent_construct=construct)

    def get_activity_type_id(self, activity_type):
        type_row = ActivityType.query.filter(ActivityType.name == activity_type).one_or_none()
        if type_row is None:
            raise AssertionError(f'Non-existing activity type {activity_type}')

        return type_row.id

    # ---- Survey  ---- #
    def add_survey(self, title, collection_id, questions, comments, description="", visibility="T", properties=None):
        survey_type_id = self.get_activity_type_id("survey")

        if properties is None:
            properties = {}

        survey = Activity(
            title=title,
            description=description,
            collection_id=collection_id,
            visibility=visibility,
            type_id=survey_type_id,
            properties=properties,
            remote_id="local"
        )

        self.db.session.add(survey)
        self.db.session.commit()

        question_relation_type = ActivityRelationType.query.filter(
            ActivityRelationType.name == "exam_question").one_or_none()

        question_construct_relation_type = ConstructActivityRelationType.query.filter(
            ConstructActivityRelationType.name == "exhibits").one_or_none()

        for index, question_data in enumerate(questions):
            if question_data.question_type[:6] == "likert":
                question = self.create_likert_question(
                    collection_id=collection_id,
                    visibility=visibility,
                    body=question_data.body,
                    prompt="",
                    location=index,
                    required=question_data.required,
                    answer_count=int(question_data.question_type[-1])
                )
            elif question_data.question_type[:2] == "mc":
                question = self.create_mc_question(
                    collection_id=collection_id,
                    visibility=visibility,
                    body=question_data.body,
                    prompt="",
                    location=index,
                    answer_type=question_data.question_type,
                    required=question_data.required
                )
            else:
                question_type_id = self.get_activity_type_id("question." + question_data.question_type)

                question = Activity(
                    title="Question " + str(index),
                    collection_id=collection_id,
                    visibility=visibility,
                    type_id=question_type_id,
                    remote_id="local",
                    properties={
                        "body": question_data.body,
                        "required": question_data.required
                    }
                )

            self.db.session.add(question)
            self.db.session.commit()

            relation = ActivityRelation(
                tail_activity_id=survey.id,
                head_activity_id=question.id,
                type=question_relation_type,
                properties={
                    "number": index
                })

            self.db.session.add(relation)

            if question_data.construct_names is not None:
                for construct_name in question_data.construct_names:
                    construct = Construct.query.filter(Construct.name == construct_name, Construct.collection_id == collection_id).one_or_none()

                    mapping = ConstructActivity(
                        construct_id=construct.id,
                        activity_id=question.id,
                        type=question_construct_relation_type,
                        properties={}
                    )
                    self.db.session.add(mapping)

                    survey_mapping = ConstructActivity.query.filter(ConstructActivity.construct_id == construct.id,
                                                                    ConstructActivity.activity_id == survey.id).one_or_none()
                    if survey_mapping is None:
                        survey_mapping = ConstructActivity(
                            construct_id=construct.id,
                            activity_id=survey.id,
                            type=question_construct_relation_type,
                            properties={}
                        )
                        self.db.session.add(survey_mapping)
                        self.db.session.commit()

            self.db.session.commit()

        if comments is not None:
            comment_type_id = self.get_activity_type_id('comment')

            comment_relation_type = ActivityRelationType.query.filter(
                ActivityRelationType.name == "exam_comment").one_or_none()

            for comment_data in comments:
                comment = Activity(
                    title='Comment ' + str(comment_data.location),
                    collection_id=collection_id,
                    visibility=visibility,
                    type_id=comment_type_id,
                    properties={
                        "body": comment_data.body
                    }
                )

                self.db.session.add(comment)
                self.db.session.commit()

                comment_relation = ActivityRelation(
                    tail_activity_id=survey.id,
                    head_activity_id=comment.id,
                    type=comment_relation_type,
                    properties={
                        "number": comment_data.location
                    }
                )

                self.db.session.add(comment_relation)

        self.db.session.commit()
        return survey

    def create_likert_question(self, collection_id, visibility, body, location, prompt="", required=True, answer_count=7):
        question_type_id = self.get_activity_type_id("question.likert")

        question = Activity(
            title="Question " + str(location),
            collection_id=collection_id,
            visibility=visibility,
            type_id=question_type_id,
            remote_id="local",
            properties={
                "body": body,
                "prompt": prompt,
                "required": required,
                "answers": self.create_likert_answers(answer_count=answer_count)
            }
        )

        return question

    def create_mc_question(self, collection_id, visibility, body, location, answer_type, prompt="", required=True):
        question_type_id = self.get_activity_type_id("question.multiple_choice")

        other_answers = []
        if answer_type == "mc_yes_no":
            other_answers = ["""
        {"en":"
            Yes
        ",
        "nl":"
            Ja
        "}
        """,
        """
        {"en":"
            No
        ",
        "nl":"
            Nee
        "}
        """]
        elif answer_type == "mc_learning_focus":
            other_answers = ["""
        {"en":"
            I believe I reached my PB
        ",
        "nl":"
            Ik denk dat ik mijn PT heb behaald
        "}
        """,
        """
        {"en":"
            I think I just missed out
        ",
        "nl":"
            Ik denk dat ik het net niet heb behaald
        "}
        """,
        """
        {"en":"
            I didn't get close to my PB
        ",
        "nl":"
            Ik kwam niet in de buurt van mijn PT
        "}
        """]
        elif answer_type == "mc_1":
            other_answers = ["""
        {"en":"
            Educational Sciences
        ",
        "nl":"
            Onderwijswetenschappen
        "}
        """,
        """
        {"en":"
            Cultural Anthropology
        ",
        "nl":"
            Culturele Antropologie
        "}
        """,
        """
        {"en":"
            Psychology
        ",
        "nl":"
            Psychologie
        "}
        """,
        """
        {"en":"
            Biomedical Sciences
        ",
        "nl":"
            Biomedische wetenschappen
        "}
        """,
        """
        {"en":"
            Information Sciences
        ",
        "nl":"
            Informatiekunde
        "}
        """,
        """
        {"en":"
            Computing Sciences
        ",
        "nl":"
            Informatica
        "}
        """,
        """
        {"en":"
            Human Geography and Spatial Planning
        ",
        "nl":"
            Sociale Geografie en Planologie
        "}
        """,
        """
        {"en":"
            Economics
        ",
        "nl":"
            Economie
        "}
        """,
        """
        {"en":"
            Law
        ",
        "nl":"
            Rechtsgeleerdheid
        "}
        """,
        """
        {"en":"
            Veterinary Medicine
        ",
        "nl":"
            Diergeneeskunde
        "}
        """]
        elif answer_type == "mc_2":
            other_answers = ["Bachelor 1", "Bachelor 2", "Bachelor 3", "Master"]
        elif answer_type == "mc_3":
            other_answers = [
        """
        {"en":"
            Female
        ",
        "nl":"
            Vrouw
        "}
        """,
        """
        {"en":"
            Male
        ",
        "nl":"
            Man
        "}
        """,
        """
        {"en":"
            Other / none / don’t want to say
        ",
        "nl":"
            Anders / geen / zeg ik liever niet
        "}
        """]

        answers = []
        for i, answer_body in enumerate(other_answers):
            answers.append(self.create_answer(i, answer_body))

        question = Activity(
            title="Question " + str(location),
            collection_id=collection_id,
            visibility=visibility,
            type_id=question_type_id,
            remote_id="local",
            properties={
                "body": body,
                "prompt": prompt,
                "required": required,
                "answers": answers
            }
        )

        return question

    def create_likert_answers(self, answer_count=7):
        if answer_count == 7:
            bodies = [
            """
            {"en":"
                Disagree Strongly
            ",
            "nl":"
                Sterk mee oneens
            "}
            """,
            """
            {"en":"
                Disagree
            ",
            "nl":"
                Mee oneens
            "}
            """,
            """
            {"en":"
                Disagree Somewhat
            ",
            "nl":"
                Een beetje oneens
            "}
            """,
            """
            {"en":"
                Neither Agree nor Disagree
            ",
            "nl":"
                Neutraal
            "}
            """,
            """
            {"en":"
                Agree Somewhat
            ",
            "nl":"
                Een beetje eens
            "}
            """,
            """
            {"en":"
                Agree
            ",
            "nl":"
                Mee eens
            "}
            """,
            """
            {"en":"
                Agree Strongly
            ",
            "nl":"
                Sterk mee eens
            "}
            """]
        elif answer_count == 5:
            bodies = [
            """
            {"en":"
                Disagree Strongly
            ",
            "nl":"
                Sterk mee oneens
            "}
            """,
            """
            {"en":"
                Disagree
            ",
            "nl":"
                Mee oneens
            "}
            """,
            """
            {"en":"
                Neither Agree nor Disagree
            ",
            "nl":"
                Neutraal
            "}
            """,
            """
            {"en":"
                Agree
            ",
            "nl":"
                Mee eens
            "}
            """,
            """
            {"en":"
                Agree Strongly
            ",
            "nl":"
                Sterk mee eens
            "}
            """]
        else:
            bodies = []

        answers = []
        for index, body in enumerate(bodies):
            answers.append(self.create_answer(index, body))

        return answers

    def create_answer(self, id, body):
        answer = {
            "id": id,
            "body": body
        }

        return answer


# When run as script create survey
if __name__ == '__main__':
    # make simple app
    app = create_minimal_app(config_obj=get_config())
    app.app_context().push()

    # create meta-db
    db.init_app(app)

    mock = MockSurvey(db)
    mock.create_survey()
