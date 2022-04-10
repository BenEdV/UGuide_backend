#!/usr/bin/env python2.7
"""
Takes the general api json definition of an exam and generates results for that exam
"""
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "-o", "--result_file", type=str,
    help='The file where the persons JSON obect should be saved')
parser.add_argument(
    "-s",
    "--num_students",
    type=int,
    help="The number of students to generate persons for")
args = parser.parse_args()

num_students = args.num_students if args.num_students is not None else 1

persons = list()

for student in range(3, num_students + 3):
    person = {
        "remote_user_id": "mock_{}".format(student),
        "name": "Mock {}".format(student),
        "role": "student",
        "mail": "m{}@test.nl".format(student),
        "institution_id": "mock_{}".format(student)
    }
    persons.append(person)

with open(args.result_file, 'w') as f:
    json.dump(persons, f)
