import uuid

import bcrypt
from flask import request
from flask_restplus import Resource, abort, fields, marshal

from create_api import api_auth_ns as ns
from learnlytics.api.models.authentication import encode_auth_token
from learnlytics.api.models.authorization import authorize_gen_api
from learnlytics.api.restplus_models import post_auth_fields, post_register_key_fields
from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize
from learnlytics.extensions import db
from learnlytics.database.api import APIKey, PermissionGenAPI
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.studydata.course import Course


@ns.route('/')
@ns.expect(post_auth_fields)
@ns.response(201, "Successfully logged in.")
@ns.response(400, "Could not log in.")
@ns.response(404, "API key does not exist.")
class Authentication(Resource):
    """
    User Login Resource
    """
    @staticmethod
    def post():
        """
        Create a JWT token from an api_key
        :return: correct response based on action (not) taken
        """
        # get the post data
        post_data = request.get_json()
        if "api_key" not in post_data or post_data["api_key"] is None:
            abort(400, "No Api Key provided")
        # fetch the user data
        existing_keys = db.session.query(APIKey).all()
        key_id = None
        current_key = post_data["api_key"].encode("ascii", "ignore")
        for key in existing_keys:
            db_key = key.key.encode("ascii", "ignore")
            key_exists = bcrypt.checkpw(current_key, db_key)
            if key_exists:
                key_id = key.id
                continue
        if key_id:
            auth_token = encode_auth_token(current_key)
            if auth_token:
                data = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode('utf-8')
                }
                return data, 200
            else:
                data = {
                    'status': 'failure',
                    'message': 'Could not log in'
                }
                return data, 400
        else:
            data = {
                'status': 'failure',
                'message': 'API key does not exist.'
            }
            return data, 404


@ns.route('/registerkey')
@ns.expect(post_register_key_fields)
@ns.response(201, "Successfully registered key.")
@ns.response(400, "Could not log in.")
@ns.response(404, "API key does not exist.")
class KeyRegistration(Resource):
    """
    API Key generation resource
    """
    @auth_required
    def post(self):
        """
        Post the user information to the server to create an api key
        :param course_code: The course that the api_key can alter
        :param requester: Used for logging
        :return: api key (a uuid)
        """
        post_data = request.get_json()
        requester = post_data.get("requester")

        authorize(Collection.get_root_collection(required=True), ["generate_api_key"])

        # Generate random API key
        api_key_uuid = uuid.uuid4()

        if not requester:
            abort(400, "No requester provided")

        APIKey.add_api_key(api_key_uuid, requester)

        return {"api_key": str(api_key_uuid)}


@ns.route('/permissions')
class KeyPermissions(Resource):
    """
    Retrieve the permissions for the api_key given.
    """
    fields_per = {"id": fields.Integer(),
                  "permission_name": fields.String()}

    def get(self):
        """
        Gets the possible permissions on the GenAPI
        :return: A list consisting of the possible permissions on the GenAPI
        """
        pass
        # token = request.headers.get("Authorization")
        # if not auhorize_gen_api(token[4:]):
        #     abort(403, "Access denied")
        # result = []
        # for permission in PermissionGenAPI.query.filter().all():
        #     result.append(marshal(permission, self.fields_per))
        # return result
