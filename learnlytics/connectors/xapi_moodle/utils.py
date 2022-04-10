# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course (3 4)
# (C) Copyright Utrecht University (Department of Information and Computing Sciences)

from flask import current_app


def get_object_id(activity):
    return activity.remote_id.split("_")[1]
