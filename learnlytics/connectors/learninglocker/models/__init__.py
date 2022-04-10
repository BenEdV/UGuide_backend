"""
Opens the various models for external use
"""


class LearningLockerSubModel(object):
    """
    Parent class for the models for interacting with Learning Locker API
    """

    def __init__(self, connector):
        self.connector = connector
