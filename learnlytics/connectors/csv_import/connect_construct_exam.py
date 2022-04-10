
import csv
from flask_restplus import abort

from learnlytics.extensions import db
from learnlytics.database.construct import Construct, ConstructActivity, ConstructActivityRelationType
import learnlytics.database.studydata as md


def connect_constructs_to_exam(csv_file, exam_id):
    """
    :param exam_id: The activitiy_id of the exam
    """
    exam = md.Activity.get(exam_id, required=True)

    questions = {}
    for relation in md.ActivityRelation.query.filter(md.ActivityRelation.tail_activity_id == exam_id).all():
        number = relation.properties["number"]
        questions[number] = md.Activity.get(relation.head_activity_id, required=True)

    reader = csv.DictReader(csv_file, delimiter=",")

    mappings = {}

    for row in reader:
        construct_name = row["ConstructName"]
        answer_letter = row.get("Answer", "")
        question_number = int(row["Question"])
        value = int(row.get("Value", 1))

        if construct_name not in mappings:
            mappings[construct_name] = {}
        if question_number not in mappings[construct_name]:
            mappings[construct_name][question_number] = []
        mappings[construct_name][question_number].append((answer_letter, value))

    for construct_name, dic in mappings.items():
        construct = Construct.query.filter(
            Construct.name == construct_name, Construct.collection_id == exam.collection_id).one_or_none()
        if construct is None:
            abort(401, f"Construct with name {construct_name} could not be found")

        for question_number, pairs in dic.items():
            properties = {
                "value_pairs": {}
            }
            for answer_letter, value in pairs:
                properties["value_pairs"][answer_letter] = value

            if construct.type.name == "concept":
                type_id = ConstructActivityRelationType.query.filter(
                    ConstructActivityRelationType.name == "tests").one().id
                if questions[question_number].type.name in ["question.multiple_choice", "question.multiple_selection"]:
                    for answer in questions[question_number].properties["answers"]:
                        if answer["id"] == answer_letter and not answer["correct"]:
                            abort(401, f"{construct_name} is a concept and can not be linked to incorrect answer {question_number}{answer_letter}")  # noqa
            if construct.type.name == "misconception":
                type_id = ConstructActivityRelationType.query.filter(
                    ConstructActivityRelationType.name == "exhibits").one().id
                if questions[question_number].type.name in ["question.multiple_choice", "question.multiple_selection"]:
                    for answer in questions[question_number].properties["answers"]:
                        if answer["id"] == answer_letter and answer["correct"]:
                            abort(401, f"{construct_name} is a misconception and can not be linked to correct answer {question_number}{answer_letter}")  # noqa

            mapping = ConstructActivity(
                construct_id=construct.id,
                activity_id=questions[question_number].id,
                type_id=type_id,
                properties=properties
            )

            db.session.add(mapping)

    db.session.commit()
