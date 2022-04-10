"""
This file contains the TokenIssuer class which is an extensions of the JWT class of the flask-jwt package.
It is extended so that it can handle multiple IdenityProviders objects instead of single authentication and identity
function
"""
from flask import request, current_app, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, \
    set_refresh_cookies, unset_jwt_cookies, get_jwt_identity, get_csrf_token, set_access_cookies
from flask_restplus import fields, abort, marshal

from learnlytics.authentication.providers.identity_provider import IdentityProvider
from learnlytics.authentication.util import current_identity, _initialise_providers
from learnlytics.models.user_settings import CourseUserSettings as UserSettingsModel

CONFIG_DEFAULTS = {
    "JWT_AUTH_CLASS_KEY": 'idp',
    "JWT_AUTH_DEFAULT_IDP": "test.json"
}

auth_required = jwt_required


user_resource_fields = {
    "id": fields.Integer(),
    "display_name": fields.String(),
    "first_name": fields.String(),
    "last_name": fields.String(),
    "idp": fields.String(),
    "institution_id": fields.String(),
    "mail": fields.String(),
    "access_csrf": fields.String(),
    "refresh_csrf": fields.String(),
    "settings": fields.Raw()
}


class AuthenticationManager(JWTManager):  # pylint: disable=too-many-instance-attributes
    """
    Authentication manager that enables an application to authenticate the user and return an JWT token using multiple
    IdentityProviders.
    Extension of the Flask-JWT object. Extended it with functions so that it can handle multiple IdentityProviders and
    each request is redirected to the right authentication and identity functions
    """

    app = None
    providers = dict()
    providers_info = dict()

    def __init__(self, identity_providers_loader=None, app=None, load_user_func=None,
                 add_user_func=None, custom_payload_extender=None):
        # pylint: disable=too-many-arguments
        """
        Constructor of AuthenticationManager
        :param identity_providers_loader: function loading IdentityProviders from config
        :param app: Flask application object
        :param load_user_func: function that loads the user based on IdentityProvider key and username
        :param add_user_func: function that adds the user based on IdentityProvider key and username, and returns it
        :param custom_payload_extender: (optional) function that receives payload and identity and adds custom fields
         to the payload
        """
        super(AuthenticationManager, self).__init__()
        if identity_providers_loader is None:
            self.identity_providers_loader = _initialise_providers
        else:
            self.identity_providers_loader = identity_providers_loader

        self.add_user_func = add_user_func
        if self.add_user_func is None:
            self.add_user_func = _default_add_user_func

        if custom_payload_extender is None:
            self.custom_payload_extender = lambda x, _: x
        else:
            self.custom_payload_extender = custom_payload_extender

        self.authentication_callback = self._redirect_authentication
        self.identity_callback = self._redirect_identity
        self.auth_request_callback = self._auth_request_handler
        self.refresh_callback = self._refresh_callback
        self.remove_callback = self._remove_callback

        @self.user_loader_callback_loader
        def user_loader(*args, **kwargs):
            return load_user_func(args[0])

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Function that sets default settings and loads providers using config from application object
        :param app: Flask application object
        :raises ValueError: when there is less than one IdentityProvider specified/loaded or a non IdentityProvider
         object is given
        """
        self.app = app
        self.providers = self.identity_providers_loader(app, self._user_loader_callback, self.add_user_func)
        if len(self.providers) == 0:
            abort(400, message=_("Minimal 1 IdentityProviders is needed"))
        else:
            for name, provider in self.providers.items():
                if not isinstance(provider, IdentityProvider):
                    abort(400, message=_("Object is not a IdentityProvider"))
                self.providers_info[name] = provider.get_provider_info()
        app.config['JWT_AUTH_URL_RULE'] = None
        app.config.setdefault("JWT_AUTH_CLASS_KEY", CONFIG_DEFAULTS["JWT_AUTH_CLASS_KEY"])
        app.config.setdefault("JWT_AUTH_DEFAULT_IDP", CONFIG_DEFAULTS["JWT_AUTH_DEFAULT_IDP"])
        super(AuthenticationManager, self).init_app(app)

    # authentication handler which also looks for identity provider identification
    def _auth_request_handler(self):
        """
        Specifies the authentication response handler function.
        :return: auhtentication response of auth_response_callback function
        :raises JWTError: when a request is invalid or invalid credentials are given
        """

        if request.headers.get('Content-Type', None) != "application/json":
            abort(400, message=_("No JSON body request header"))

        data = request.get_json()
        username = data.get("username", None)
        password = data.get("password", None)
        idp = data.get(current_app.config.get('JWT_AUTH_CLASS_KEY'), current_app.config.get('JWT_AUTH_DEFAULT_IDP'))
        criterion = [username, len(data) == 2 or len(data) == 3]

        if not all(criterion):
            abort(401, message="Invalid credentials")

        identity = self.authentication_callback(username, password, idp)

        if not identity:
            abort(401, message="Invalid credentials")

        identity.idp = idp
        if identity.mail is not None:
            access_token = create_access_token(identity=identity.mail)
            refresh_token = create_refresh_token(identity=identity.mail)
        elif identity.institution_id is not None:
            access_token = create_access_token(identity=identity.institution_id)
            refresh_token = create_refresh_token(identity=identity.institution_id)
        else:
            access_token = create_access_token(identity=identity.id)
            refresh_token = create_refresh_token(identity=identity.id)

        identity.access_csrf = get_csrf_token(access_token)
        identity.refresh_csrf = get_csrf_token(refresh_token)
        identity.settings = UserSettingsModel.get_user_settings(identity.id)

        resp = jsonify(marshal(identity, user_resource_fields))
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        return resp

    # function which checks if identity provider exists and if so it tries to login
    def _redirect_authentication(self, username, password, idp):
        """
        Function which redirects authentication request to the right authentication function
        :param username: String containing the username of the user
        :param password: String containing the password of the user
        :param idp: String containing unique IdentityProvider name
        :return: result of the authentication function if idp exists
        """
        print(self.providers)
        if idp not in self.providers:
            return None
        else:
            return self.providers[idp].authenticate(username, password)

    # function which checks if identity provider exists and if so it tries to return the right identity function
    def _redirect_identity(self, payload):
        """
        Function which redirects identity request to the right identity function
        :param payload: Dictionary containing the payload of the jwt token
        :return: the result of the identity function if idp exists
        """
        idp = payload.get(current_app.config.get('JWT_AUTH_CLASS_KEY'), current_app.config.get('JWT_AUTH_DEFAULT_IDP'))
        if idp not in self.providers:
            return None
        else:
            return self.providers[idp].identity(payload)

    def _refresh_callback(self):
        identity = get_jwt_identity()
        if identity is not None:
            access_token = create_access_token(identity=identity)
            cur_identity = current_identity()
            cur_identity.access_csrf = get_csrf_token(access_token)
            cur_identity.settings = UserSettingsModel.get_user_settings(cur_identity.id)

            resp = jsonify(marshal(cur_identity, user_resource_fields))
            set_access_cookies(resp, access_token)
            return resp
        else:
            abort(401, message="Invalid credentials")

    def _remove_callback(self):
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp


def _default_load_user_func(provider, user_id):
    user = object()
    setattr(user, "id", user_id)
    setattr(user, "idp", provider)
    return user


def _default_add_user_func(provider, user_id, **kwargs):  # pylint: disable=unused-argument
    return _default_load_user_func(provider, user_id)
