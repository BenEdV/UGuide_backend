#!/usr/bin/env python3
"""
Populates the database with students, courses, exams, concepts and results
"""
import os
import argparse
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from learnlytics.app import create_minimal_app  # noqa
from learnlytics.extensions import db  # noqa
from mock_data.mock_data3 import MockDatabase  # noqa
from config import get_config  # noqa

parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--num_students",
    type=int,
    help="The number of students to be instantiated in the database")
parser.add_argument(
    "-g",
    "--num_groups",
    type=int,
    help="The number of groups per course to be instantiated in the database")
parser.add_argument(
    "-p",
    "--participation_rate",
    type=int,
    help="The rate at which students participate in exams 1--100, default 100.")
args = parser.parse_args()

num_students = args.num_students if args.num_students is not None else 40
num_groups = args.num_groups if args.num_groups is not None else 4
participation_rate = args.participation_rate if args.participation_rate is not None else 100

# make simple app
app = create_minimal_app(config_obj=get_config())
app.app_context().push()

# create meta-db
db.init_app(app)

# fill meta-db with mock data
try:
    MockData = MockDatabase(db)
    MockData.fill_data(num_students, num_groups, participation_rate)
except Exception as e:
    import traceback
    traceback.print_exc()
    print("Unexpected error undoing changes: " + str(e.message))

    db.session.rollback()
finally:
    # Removes the session
    db.session.remove()
