"""
This module contains various utility functions to be used in the Remindo connector
"""

from flask import current_app


def get_object_id(activity):
    return f"https://{current_app.config['BASE_URL']}/activities/{activity.id}"
