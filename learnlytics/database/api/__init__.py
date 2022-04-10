# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course (3 4)
# (C) Copyright Utrecht University (Department of Information and Computing Sciences)
"""
This module contains all database definition for the general api in the database
"""

from learnlytics.database.api.apikey import *


def add_gen_api_permissions():
    from learnlytics.api.models.authorization import add_permissions
    add_permissions([
        "add_exam", "add_exam_result", "add_person"
    ])
