
import csv

import learnlytics.authorization.manager as auth
from learnlytics.extensions import db
from learnlytics.database.authorization.role import Role
from learnlytics.database.authorization.user import User, UserPassHash


def add_new_users(csv_file, collection_id):
    """
    Takes the students in the given csv file and adds creates new users if they do not exist and add them to the
    collection with the given collection_id.
    """

    students = []
    # with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csv_file, delimiter=",")
    for row in reader:
        first_name = row["Roepnaam"]
        last_name = row["Achternaam"]
        if row["Voorvoegsels"]:
            last_name = last_name + ", " + row["Voorvoegsels"]
            name = first_name + " " + row["Voorvoegsels"] + " " + row["Achternaam"]
        else:
            name = first_name + " " + last_name

        # Add student if doesn't already exist
        student = User.query.filter(User.institution_id == row["Studentnummer"]).one_or_none()
        if student is None:
            student = User(
                row["Studentnummer"],
                name,
                row.get("mail", None),
                first_name,
                last_name
            )
            db.session.add(student)
            db.session.flush()
            db.session.add(UserPassHash(
                student.id,
                row["Achternaam"][0:2].lower() + row["Studentnummer"]))
        students.append(student)

    member_role = Role.get_name("member")
    student_role = Role.get_name("student")

    for student in students:
        auth.add_user_role(student.id, student_role.id, collection_id)
        auth.add_user_role(student.id, member_role.id, collection_id)
