"""
Module containing ldap provider implementation of an Identityprovider
"""

from gettext import gettext as _

from ldap3 import Connection, Server, ALL, ALL_ATTRIBUTES

from learnlytics.authentication.providers.identity_provider import IdentityProvider

CONFIG_DEFAULTS = {
    'USE_SLL': False,
    'GET_INFO': ALL,
    'USERNAME_TEMPLATE': '{}',
    'PORT': None,
    'BASE_DN': 'DC=example,DC=com'
}


class LdapProvider(IdentityProvider):
    """
    Implementation of an IdentityProvider which authenticates the user using an LDAP server, implemented with ldap3
    library
    """

    def __init__(self, name, user_loader, user_adder, config):
        if 'ADDRESS' not in config:
            raise ValueError(_("ADDRESS is minimal settings needed for ldap but is missing"))
        for key, value in CONFIG_DEFAULTS.items():
            config.setdefault(key, value)
        super(LdapProvider, self).__init__(name)
        self.server = Server(config['ADDRESS'], port=config['PORT'], use_ssl=config['USE_SLL'],
                             get_info=config['GET_INFO'])
        self.usernametemplate = config['USERNAME_TEMPLATE']
        self._user_loader_callback = user_loader
        self._user_adder = user_adder
        self.base_dn = config['BASE_DN']

    def authenticate(self, username, password):
        """
        Given an LDAP username and password, connect to the LDAP server
        to check credentials
        :param username: String containing the username of the user
        :param password: String containing the password of the user
        :return: if successful: User object of the user
        """
        if username is None or password is None:
            return None
        user = self.usernametemplate.format(username)
        connection = Connection(self.server, user=user, password=password)

        if connection.bind():
            display_name = username
            mail = ''

            # Try to find the principal in the directory, returning all attributes
            connection.search(self.base_dn, '(CN=' + username + ')', attributes=ALL_ATTRIBUTES)
            if connection.entries.__len__() == 1:
                # If found, set attributes
                display_name = str(connection.entries[0].displayName)
                mail = str(connection.entries[0].mail)

            user = self._user_loader_callback(self.name, username)
            if user is None:
                user = self._user_adder(self.name, username, display_name, mail)
            return user

    def identity(self, payload):
        """
        Given a JWT Payload, containing the LDAP identity,
        get the identity information from the LDAP server
        :param payload: Dictionary of the payload of the token
        :return: The User object of the user
        """
        server, name = super(LdapProvider, self).identity(payload)
        return self._user_loader_callback(server, name)
