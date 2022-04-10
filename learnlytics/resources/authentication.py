"""
This module contains the resources for logging in and registering new users
"""

from flask import request, current_app
from flask_jwt_extended import jwt_refresh_token_required
from flask_restplus import fields, Resource, abort

from create_api import authenticationns as ns
from learnlytics.authentication.authentication_manager import auth_required
from learnlytics.authentication.util import current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.database.authorization.user import add_user
from learnlytics.resources.restplus_models.expect_models import auth_fields, reg_fields


def _get_jwt():
    return current_app.extensions["flask-jwt-extended"]


@ns.route('/')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class AuthResource(Resource):
    """
    Resource exposing a list of IdentityProvider information objects through get and through post authentication and
    token renewal
    """
    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        """
        Gets the authentication providers which are available.
        - __:return:__ An array with the names of the available providers.
        """
        _jwt = _get_jwt()
        return _jwt.providers_info

    @ns.expect(auth_fields, validation=True)
    @ns.response(200, 'Success')
    def post(self):  # pylint: disable=no-self-use
        """
        Authenticates user via password and username or renew token when request contains valid token
        - __:return:__ A valid access token when successful otherwise an JWT error message
        """
        _jwt = _get_jwt()
        return _jwt.auth_request_callback()


@ns.route('/refresh')
@ns.response(401, 'Unauthorized')
class AuthRenewalResource(Resource):
    """
    Resource exposing a token renewal function through post
    """

    @ns.expect(auth_fields)
    @ns.response(200, 'Success')
    @jwt_refresh_token_required
    def post(self):  # pylint: disable=no-self-use
        """
        Authenticates user via password and username or renew token when request contains valid token
        - __:return:__ A valid access token when successful otherwise an JWT error message
        """
        _jwt = _get_jwt()
        return _jwt.refresh_callback()


@ns.route('/remove')
@ns.response(401, 'Unauthorized')
class AuthRemovalResource(Resource):
    """
    Resource exposing a token renewal function through post
    """

    @ns.expect(auth_fields)
    @ns.response(200, 'Success')
    def post(self):  # pylint: disable=no-self-use
        """
        Remove authentication cookies
        - __:return:__ A valid access token when successful otherwise an JWT error message
        """
        _jwt = _get_jwt()
        return _jwt.remove_callback()


@ns.route('/resetpassword')
@ns.response(401, 'Unauthorized')
class AuthResetResource(Resource):
    """
    Allows a user to reset their own password
    """

    reset_fields = ns.model("reset_own", {
        'oldPassword': fields.String(required=True, example="oldPoorPassword"),
        'newPassword': fields.String(required=True, example="G00dN3WpAsSW0rd!")})

    @auth_required
    @ns.expect(reset_fields)
    @ns.response(200, 'Success')
    def post(self):  # pylint: disable=no-self-use
        """
        Checks if the old password is correct and if so resets the password of current user to the given new password
        """
        user = current_identity()
        data = request.json

        from learnlytics.database.authorization.user import UserPassHash
        import bcrypt

        pass_hash = UserPassHash.query.get(user.id)
        if not bcrypt.checkpw(data["oldPassword"].encode('utf-8'), pass_hash.hash.encode('utf-8')):
            abort(401, message="Incorrect old password")
        pass_hash.reset_password(data["newPassword"])


@ns.route('/resetpassword/<user_id>')
@ns.response(401, 'Unauthorized')
class AuthResetOtherResource(Resource):
    """
    Allows a user's password to be reset
    """

    reset_fields = ns.model("reset", {
        'newPassword': fields.String(required=True, example="G00dN3WpAsSW0rd!")})

    @auth_required
    @ns.expect(reset_fields)
    @ns.response(200, 'Success')
    def post(self, user_id):  # pylint: disable=no-self-use
        """
        Set the given user's password to the new password given in the body
        """
        from learnlytics.database.authorization.collection import Collection

        root = Collection.get_root_collection(required=True)
        authorize(root, ["reset_user_password"])

        from learnlytics.database.authorization.user import UserPassHash, User
        user = User.get(user_id, required=True)
        data = request.json

        pass_hash = UserPassHash.query.get(user.id)
        pass_hash.reset_password(data["newPassword"].encode('utf-8'))


@ns.route('/register')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class RegisterResource(Resource):
    """
    Resource for creating new accounts
    """
    @ns.expect(reg_fields, validation=True)
    @ns.response(200, 'Success')
    def post(self):  # pylint: disable=no-self-use
        """
        Authenticates user via password and username or renew token when request contains valid token
        - __:return:__ A valid access token when successful otherwise an JWT error message
        """
        data = request.json

        import requests
        captcha_data = {
            "secret": current_app.config.get("CAPTCHA_SECRET"),
            "response": data["captcha_token"]
        }
        captcha_verify = requests.post("https://www.google.com/recaptcha/api/siteverify", data=captcha_data)
        if not captcha_verify.json()["success"]:
            abort(401, message="Captcha failed")

        from learnlytics.extensions import db
        from learnlytics.database.authorization.user import UserPassHash, User

        if User.query.filter(User.mail == data["email"]).one_or_none():
            abort(401, message="Email already exists")

        if len(data["password"]) < 6:
            abort(401, message="Passwords must be at least 6 characters in length")

        new_user = add_user(first_name=data["first_name"],
                            last_name=data["last_name"],
                            display_name=data.get("display_name", data["first_name"] + " " + data["last_name"]),
                            mail=data["email"],
                            institution_id=data["institution_id"])

        db.session.add(UserPassHash(new_user.id, data["password"]))
        db.session.commit()

        import learnlytics.authorization.manager as auth
        from learnlytics.database.authorization.role import Role

        role = Role.query.filter(Role.name == "student").one_or_none()
        auth.add_user_role(new_user.id, role.id, 1)

        return 200
