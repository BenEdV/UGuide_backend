"""
Module containing saml provider implementation of an Identityprovider
"""
import base64
import csv
import json
import requests

from learnlytics.authentication.providers.identity_provider import IdentityProvider
from learnlytics.database.authorization.role import Role

CONFIG_DEFAULTS = {
    "HOST": None,
    "CLIENTID": None,
    "CLIENTSECRET": None
}


# load authentication and authorization
def oauth_add_user(server, name, full_name, mail):
    """
    Function that adds the user to the database
    :param server: key of the IdentityProvider authenticating this user
    :param name: id of the user
    :param full_name: full name of the user
    :param mail: email of the user
    :return: User object that was added
    """
    from learnlytics.database.authorization.user import User
    import learnlytics.authorization.manager as auth
    from learnlytics.extensions import db

    user = User(institution_id=name, display_name=full_name, mail=mail)
    db.session.add(user)
    db.session.commit()

    return user


class OAuthProvider(IdentityProvider):
    """
    Implementation of an IdentityProvider which authenticates the user using SAML
    """

    def __init__(self, name, user_loader, user_adder, config):
        if any(k not in config for k in ('HOST', 'CLIENTID', 'CLIENTSECRET', 'REDIRECT_URI')):
            raise ValueError(
                "HOST, CLIENTID, CLIENTSECRET, REDIRECT_URI is minimal settings needed for saml but is missing"
            )
        for key, value in CONFIG_DEFAULTS.items():
            config.setdefault(key, value)
        super(OAuthProvider, self).__init__(name)

        self._user_loader_callback = user_loader
        self._user_adder = oauth_add_user
        self.host = config['HOST']
        self.client_id = config['CLIENTID']
        self.client_secret = config['CLIENTSECRET']
        self.redirect_uri = config['REDIRECT_URI']

    def authenticate(self, username, password):
        """
        Given an SAML access code (username), connect to the SAML server
        to check credentials
        :param username: String containing the access code of the user
        :param password: Unused
        :return: if successful: User object of the user
        """
        print(self.host, self.client_id, self.client_secret, self.redirect_uri)
        if username is None or password is None:
            return None

        CREDENTIALS = base64.b64encode(
            self.client_id.encode('ascii') + b":" + self.client_secret.encode('ascii')
        ).decode("ascii")

        token_url = self.host + "/oauth/token"
        formdata = {
            'grant_type': 'authorization_code',
            'code': username,
            'redirect_uri': self.redirect_uri
        }

        headers = {
            "Authorization": f"Basic {CREDENTIALS}",
            "Content-type": "application/x-www-form-urlencoded"
        }
        response = requests.post(
            url=token_url,
            headers=headers,
            data=formdata,
        )
        print(response.content)
        response_data = response.json()
        if "id_token" not in response_data:
            print(response.content)
            return

        claim = response_data["id_token"].split('.')
        # add padding to base64 string
        claim[1] = claim[1].replace("_", "/")
        claim[1] += "=" * ((4 - len(claim[1]) % 4) % 4)
        print(claim[1])
        user_data = base64.b64decode(claim[1])
        response_data["user"] = json.loads(user_data)
        print(response_data)
        if response_data["user"]:
            display_name = response_data["user"]["nickname"]
            student_id = response_data["user"].get("studentNumber", None)
            username = response_data["user"].get("name", None)

            if student_id is not None:
                institution_id = student_id
            else:
                institution_id = username

            mail = response_data["user"]["email"].lower()
            if not isinstance(mail, str) or len(mail) > 100:
                mail = None

            if mail is not None:
                user = self._user_loader_callback(mail)
            else:
                user = self._user_loader_callback(student_id)

            if user is None:
                user = self._user_adder(self.name, student_id, display_name, mail)

            return user

    def identity(self, payload):
        """
        Given a JWT Payload, containing the LDAP identity,
        get the identity information from the LDAP server
        :param payload: Dictionary of the payload of the token
        :return: The User object of the user
        """
        server, name = super(OAuthProvider, self).identity(payload)
        return self._user_loader_callback(server, name)
