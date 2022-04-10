"""
This file contains an plaintext implementation of an Identityprovider, should only be used for testing purposes
"""
from learnlytics.authentication.providers.identity_provider import IdentityProvider


class PlainTextProvider(IdentityProvider):
    """
    Implementation of an IdentityProvider which authenticates the user from a plain text config (For test purposes only)
    """

    def __init__(self, name, user_loader, user_adder, config=None):
        super(PlainTextProvider, self).__init__(name)
        if config is None:
            config = {}
        self.users = config.get("Users")
        self._user_loader_callback = user_loader
        self._user_adder = user_adder

    def authenticate(self, username, password):
        """
        Authenticate the user
        :param username: String containing the username of the user
        :param password: String containing the password of the user
        :return: if successful: User object of the user
        """

        if (username in self.users) and self.users[username] == password:
            user = self._user_loader_callback(self.name, username)
            if user is None:
                user = self._user_adder(self.name, username, username, '')
            return user

    def identity(self, payload):
        """
        Based on payload of token return the User object of the user
        :param payload: Dictionary of the payload of the token
        :return: The User object of the user
        """
        server, name = super(PlainTextProvider, self).identity(payload)
        return self._user_loader_callback(server, name)
