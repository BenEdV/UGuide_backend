#!/usr/bin/env python2.7
"""
Takes a json file output of students call and generates a CSV
"""
import os
import argparse
import random
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    'infile', metavar='infile', type=str,
    help='The input file sql')
# parser.add_argument(
#     'outfile', metavar='outfile', type=str,
#     help='The output file sql')
args = parser.parse_args()


# First pass collect ids
with open(args.infile, 'r') as f:
    data = json.load(f)

# print headers
row = ["First name", "Last name", "Tussenvoegsel", "Student id"]
for concept in data[0]["concepts"]:
    row.append(concept["name"].replace(",", "") + ("!" if concept["is_misconcept"] else ""))
print(", ".join(row))

for student in data:
    row = []
    row.append(student["first_name"])
    row.append(student["last_name"] + ("" if "," in student["last_name"] else ", "))
    row.append(student["id"])
    for concept in student["concepts"]:
        row.append(unicode(concept["score"]))

    print(", ".join(row).encode('utf-8'))
