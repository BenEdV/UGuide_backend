#!/usr/bin/env python2.7
"""
Adds the user data to the meta-database
arg 1: The name of csv file
"""

import csv
import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_config  # noqa
from learnlytics import create_minimal_app  # noqa

import learnlytics.authorization.manager as auth  # noqa
from learnlytics.database import init_db, db  # noqa
from learnlytics.database.authorization.user import User, UserPassHash  # noqa
import learnlytics.database.studydata as md  # noqa

# make simple app, using the SQLAlchemy config
app = create_minimal_app(config_obj=get_config())

# create meta-db
init_db(app, new=True)


app_context = app.app_context()
app_context.push()

csv_file = sys.argv[1]
if not os.path.isfile(csv_file):
    print("The given file does not exist")
    sys.exit(1)
course_name = raw_input("The name of the course: ")
course_code = raw_input("The code of the course: ")
course_start_date = datetime.strptime(raw_input("The start date of the course YYYY/MM/DD: "), "%Y/%m/%d").date()
course_end_date = datetime.strptime(raw_input("The end date of the course YYYY/MM/DD: "), "%Y/%m/%d").date()
course_parent_id = raw_input("The id of the parent collection: ")
teacher_name = raw_input("The name of the teacher of the course: (display_name in db)")

db = db
app = app
students = list()
try:
    teacher = User.query.filter(User.display_name == teacher_name).one_or_none()
    if teacher is None:
        print("No user could be found with name: " + teacher_name)
        sys.exit(1)

    print("Adding course...")
    course = md.Course(
        name=course_name,
        collection_parent_id=course_parent_id,
        code=course_code,
        start_date=course_start_date,
        end_date=course_end_date
        )

    db.session.add(course)
    db.session.flush()

    print("Adding users...")

    # Use the CSV file given as first parameter of command
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            first_name = row["Roepnaam"]
            last_name = row["Achternaam"]
            if row["Voorvoegsels"]:
                last_name = last_name + ", " + row["Voorvoegsels"]
                name = first_name + " " + row["Voorvoegsels"] + " " + row["Achternaam"]
            else:
                name = first_name + " " + last_name

            # Add student if doesn't already exist
            student = User.get("local_" + row["Studentnummer"], required=False)
            if student is None:
                student = User(int(row["Studentnummer"]), "local", name, row["mail"], first_name, last_name)
                db.session.add(student)
                db.session.flush()
                db.session.add(UserPassHash(
                    "local_" + row["Studentnummer"],
                    row["Achternaam"][0:2] + str(row["Studentnummer"])))
            students.append(student)

            # Add group if doesn't already exist
            group = md.UserGroup.query.filter(
                md.UserGroup.course_id == course.id,
                md.UserGroup.name == row["Groep"]).one_or_none()
            if group is None:
                group = md.UserGroup.add_group(course=course, name=row["Groep"])
                db.session.flush()
            md.UserGroup.add_student(group, student)

    print("Linking users to courses...")
    # link students to course
    for student in students:
        student.courses.append(course)
        auth.add_user_role(student.key, "student", course.collection_id)

    # link teacher to course
    auth.add_user_role(teacher.key, "teacher", course.collection_id)

    print("Committing to database...")
    db.session.commit()

except Exception as e:
    import traceback
    traceback.print_exc()
    print("Unexpected error undoing changes:", e.message)

    db.session.rollback()
finally:
    # Removes the session
    db.session.remove()
