"""
This file contains the abstract base class, IdentityProvider, for concrete implementations
"""
from abc import ABCMeta, abstractmethod


class IdentityProvider(object):
    """
    Abstract class for Identityproviders
    """
    __metaclass__ = ABCMeta

    def __init__(self, name, info=None):
        self.name = name
        self.info = info

    @abstractmethod
    def authenticate(self, username, password):
        """
        Authenticate the user
        :param username: String containing the username of the user
        :param password: String containing the password of the user
        :return: if successful: User object of the user
        """
        pass

    def identity(self, payload):
        """
        Based on payload of token return the User object of the user
        :param payload: Dictionary of the payload of the token
        :return: The User object of the user
        """
        identity = payload.get("identity", None)
        if identity is None:
            return None
        else:
            return self.name, identity

    def get_provider_info(self):
        """
        Function returning information about the IdentityProvider
        :return: Dictionary containing all information about the IdentityProvider
        """
        return self.info
