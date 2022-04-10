"""
This module allows initialization of the authorization database
"""


from learnlytics.database.authorization.collection import *
from learnlytics.database.authorization.permission import *
from learnlytics.database.authorization.role import *
from learnlytics.database.authorization.user import *


def init_authorization_db_with_root(root_user_id):
    from learnlytics.authorization.manager import add_user_role
    # from learnlytics.database.authorization.role import Role

    # add root collection
    col_id = init_authorization_db()
    admin_role = Role.get_name("admin")

    add_user_role(root_user_id, admin_role.id, col_id)


def init_authorization_db():
    from learnlytics.authorization.manager import add_collection
    # add root collection
    collection = add_collection(name="Universiteit")
    return collection.id
