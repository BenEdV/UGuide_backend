"""
Module containing saml provider implementation of an Identityprovider
"""
import base64
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
def saml_add_user(server, name, full_name, mail, role):
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

    student_role = Role.get_name("student")
    auth.add_user_role(user.id, student_role.id, 1)
    return user


def set_user_access_token(server, user_id, access_token):
    from learnlytics.database.authorization.user import UserToken
    from learnlytics.extensions import db
    _user_token = UserToken.query.filter(
        UserToken.user_id == user_id,
        UserToken.identity_provider == server).one_or_none()

    if _user_token is None:
        _user_token = UserToken(user_id=user_id, identity_provider=server, token=access_token)
        db.session.add(_user_token)

    _user_token.token = access_token

    db.session.commit()


class SAMLProvider(IdentityProvider):
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
        super(SAMLProvider, self).__init__(name)

        self._user_loader_callback = user_loader
        self._user_adder = saml_add_user
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
        from learnlytics.database.authorization.user import User

        print(self.host, self.client_id, self.client_secret, self.redirect_uri)
        if username is None or password is None:
            return None

        CREDENTIALS = base64.b64encode(
            self.client_id.encode('ascii') + b":" + self.client_secret.encode('ascii')
        ).decode("ascii")

        token_url = self.host + "/token"
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
        # print(response.content)
        response_data = response.json()
        if "id_token" not in response_data:
            print(response.content)
            return

        claim = response_data["id_token"].split('.')
        # add padding to base64 string
        claim[1] += "=" * ((4 - len(claim[1]) % 4) % 4)
        user_data = base64.b64decode(claim[1])
        response_data["user"] = json.loads(user_data)
        print(response_data)
        if response_data["user"]:
            if response_data["user"]["nonce"] != password:
                print("NONCE does not match that given by user")
                return None
            display_name = response_data["user"].get("http://wso2.org/claims/givenname",
                response_data["user"]["http://wso2.org/claims/username"])
            student_id = response_data["user"].get("http://wso2.org/claims/studentNumber", None)
            username = response_data["user"].get("http://wso2.org/claims/username", None)

            if student_id is not None:
                institution_id = student_id
            else:
                institution_id = username

            mail_or_mail_list = response_data["user"]["http://wso2.org/claims/emailaddress"]
            mail = None
            if isinstance(mail_or_mail_list, list):
                for emailaddress in mail_or_mail_list:
                    existing_mail = User.query.filter(User.mail == emailaddress).one_or_none()
                    if existing_mail is not None:
                        mail = existing_mail.mail
                        break
                if mail is None: # no existing mail found, use the first one in the list
                    mail = mail_or_mail_list[0]
            elif isinstance(mail_or_mail_list, str) and len(mail_or_mail_list) <= 100:
                mail = mail_or_mail_list

            if mail is not None:
                mail = mail.lower()

            role = response_data["user"]["http://wso2.org/claims/role"]

            if mail is not None:
                user = self._user_loader_callback(mail)
            else:
                user = self._user_loader_callback(student_id)

            if user is None:
                user = self._user_adder(self.name, student_id, display_name, mail, role)

            set_user_access_token(self.name, user.id, response_data["access_token"])
            return user

    def identity(self, payload):
        """
        Given a JWT Payload, containing the LDAP identity,
        get the identity information from the LDAP server
        :param payload: Dictionary of the payload of the token
        :return: The User object of the user
        """
        server, name = super(SAMLProvider, self).identity(payload)
        return self._user_loader_callback(server, name)
