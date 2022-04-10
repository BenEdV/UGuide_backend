#!/usr/bin/env python2.7
"""
Takes the general api json definition of an exam and generates results for that exam
"""
import argparse
import random
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f", "--exam_file", type=str,
    help='The JSON file containing the general api definition of an exam')
parser.add_argument(
    "-o", "--result_file", type=str,
    help='The file where the results JSON obect should be saved')
parser.add_argument(
    "-s",
    "--num_students",
    type=int,
    help="The number of students to generate exam results for")
args = parser.parse_args()

num_students = args.num_students if args.num_students is not None else 1

# First pass collect ids
with open(args.exam_file, 'r') as f:
    data = json.load(f)

results = list()


def generate_result_for_choice_question(question, skill):
    question_result = dict()
    question_result["question_id"] = question["remote_question_id"]
    if random.randint(0, 100) < skill:
        correct_answers = list(filter(lambda x: x["correct"], question["answers"]))
        chosen_answer = random.choice(correct_answers)
    else:
        chosen_answer = random.choice(question["answers"])
    question_result["given_answer"] = chosen_answer["remote_answer_id"]
    question_result["score"] = chosen_answer["score"]

    return question_result


def generate_result_for_multiple_selection_question(question, skill):
    question_result = dict()
    question_result["question_id"] = question["remote_question_id"]
    given_answers = []
    question_result["score"] = 0
    incorrect = False

    for answer in question["answers"]:
        if answer["correct"] and random.randint(0, 100) < skill:
            given_answers.append(answer["remote_answer_id"][-1])
            question_result["score"] += answer["score"]
        elif not answer["correct"] and random.randint(0, 100) > skill:
            incorrect = True
            given_answers.append(answer["remote_answer_id"][-1])
    question_result["given_answer"] = "{" + ",".join(given_answers) + "}"

    if incorrect:
        question_result["score"] = 0

    return question_result


result_generator = {
    "multiple choice": generate_result_for_choice_question,
    "multiple selection": generate_result_for_multiple_selection_question
}

for student in range(3, num_students + 3):
    student_result = dict()
    skill = random.randint(30, 100)
    student_result["question_results"] = list()
    student_result["remote_result_id"] = "{}_r{}".format(data["remote_exam_id"], student)
    student_result["remote_user_id"] = "mock_{}".format(student)
    total_score = 0
    for question in data["questions"]:
        question_result = result_generator[question["type"]](question, skill)
        student_result["question_results"].append(question_result)
        total_score += question_result["score"]
    student_result["score"] = total_score
    student_result["grade"] = float(total_score) * 10 / len(data["questions"])
    results.append(student_result)

with open(args.result_file, 'w') as f:
    json.dump(results, f)
