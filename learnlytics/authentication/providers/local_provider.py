"""
This file contains an plaintext implementation of an Identityprovider, should only be used for testing purposes
"""
import bcrypt
from .identity_provider import IdentityProvider


class LocalProvider(IdentityProvider):
    """
    Implementation of an IdentityProvider which authenticates the user from a plain text config (For test purposes only)
    """

    def __init__(self, name, user_loader, get_pass_info, config=None):
        super(LocalProvider, self).__init__(name)
        if config is None:
            config = {}
        self.users = config.get("Users")
        self._user_loader_callback = user_loader

        from learnlytics.database.authorization.user import UserPassHash
        self.__get_userpass_info_callback = UserPassHash.get_hash

    def __get_userpass_info(self, username):
        return self.__get_userpass_info_callback(username)

    def authenticate(self, username, password):
        """
        Authenticate the user
        :param username: String containing the username of the user
        :param password: String containing the password of the user
        :return: if successful: User object of the user
        """
        if isinstance(username, int):
            # Allow only institution_id and mail login to prevent brute-force attacks
            return

        user = self._user_loader_callback(username)

        if user is None:
            return

        passw_hash = self.__get_userpass_info(user.id)
        if passw_hash is not None and bcrypt.checkpw(password.encode("utf-8"), passw_hash.encode("utf-8")):
            return user

    def identity(self, payload):
        """
        Based on payload of token return the User object of the user
        :param payload: Dictionary of the payload of the token
        :return: The User object of the user
        """
        server, user_id = super(LocalProvider, self).identity(payload)
        return self._user_loader_callback(user_id)

    @staticmethod
    def make_hash(password):
        """
        :param password: the password to hash
        :return: the hashed password
        """
        return bcrypt.hashpw(password, bcrypt.gensalt())
