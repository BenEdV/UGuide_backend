#!/usr/bin/env python3
"""
Database migration script which also creates meta database if it does not already exist
"""
import getpass

from learnlytics.app import create_minimal_app
from learnlytics.extensions import db
from learnlytics.database import add_default_rows
# from learnlytics.database import init_db, db, add_default_rows
from learnlytics.database.authorization import init_authorization_db_with_root
from learnlytics.database.authorization.user import User, UserPassHash
from learnlytics.database.connector.connector import Connector

from config import get_config

import learnlytics.database.api
import learnlytics.database.authorization
import learnlytics.database.connector
import learnlytics.database.learnlyticslogging
import learnlytics.database.studydata
import learnlytics.database.usersettings
import learnlytics.database.construct

# This script creates a new meta-database,
# creates a migrate-repo (if not yet exists),
# and fills adds root user


def prompt_user():
    """
    Get information from the user about mail, password, identityprovider and root collection_id
    :return: mail, password, identityprovider and root collection_id
    """
    correct = False
    mail = None
    passw = None
    while not correct:
        answered = False
        while not answered:
            mail = input("Please enter your root mail address: ")

            if len(mail) > 0:
                answered = True
                break

        match = False
        while not match:
            pass1 = getpass.getpass("Please enter root password: ")

            if len(pass1) < 8:
                print("Password is shorter than 8 characters")
                continue
            pass2 = getpass.getpass("Please enter root password again: ")
            if pass1 == pass2:
                match = True
                passw = pass1
                break
            else:
                print("Passwords do not match, try again")
                continue

        print("Username: " + mail)

        answered = False
        while not answered:
            check = input("Is this correct(y/n): ")

            if len(check) > 0 and (check[0] == 'n' or check[0] == 'N'):
                answered = True
                print("Ok try again")
                break
            if len(check) > 0 and (check[0] == 'y' or check[0] == 'Y'):
                answered = True
                correct = True
                break

    return mail, passw


# make simple app
app = create_minimal_app(config_obj=get_config())
app.app_context().push()

# create meta-db
# init_db(app, new=True)
db.init_app(app)
db.create_all()

add_default_rows()

# database configurations
SQLALCHEMY_DATABASE_URI = app.config.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_MIGRATE_REPO = app.config.get("SQLALCHEMY_MIGRATE_REPO")

# app_context = app.app_context()
# app_context.push()

# get mail, identityprovider, password
mail, passw = prompt_user()
# Add root user to database
user = User(mail=mail)
db.session.add(user)
db.session.flush()
id = user.id
passhash = UserPassHash(user.id, str(passw))
db.session.add(passhash)

init_authorization_db_with_root(id)

# Add connectors
learninglocker_connector = Connector(
    title="learninglocker",
    code="learninglocker",
    implementation="learninglocker",
    settings={
        "api_base_url": 'http://learninglocker_api:8080',
        "xapi_base_url": "http://learninglocker_xapi:8081/data/xAPI",
        "username": 'example@test.com',
        "password": 'abcd1234'
    })

local_connector = Connector(
    title="local",
    code="local",
    implementation="local",
    settings={}
)

db.session.add(learninglocker_connector)
db.session.add(local_connector)
db.session.commit()
