"""
Opens the various models for external use
"""


class RemindoSubModel(object):
    """
    Parent class for the models for interacting with Remindo API
    """

    def __init__(self, connector, code, settings):
        self.connector = connector
        self.code = code
        self.settings = settings
