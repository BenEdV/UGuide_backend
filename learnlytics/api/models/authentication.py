import bcrypt
import datetime
from flask import request, current_app
from flask_restplus import abort
import jwt

from learnlytics.extensions import db
from learnlytics.database.api.apikey import APIKey


def encode_auth_token(key_id):
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5, seconds=5),
        'iat': datetime.datetime.utcnow(),
        'nbf': datetime.datetime.utcnow(),
        'sub': key_id.decode("ascii"),
        'identity': "gen_api_user"
    }

    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )


def authenticate():
    token = request.headers.get("Authorization")
    if token is None:
        abort(401, "No authorization token was given in the header")
    key = authenticate_gen_api(token[4:])
    return key


def authenticate_gen_api(token):
    """
    Decodes the auth token
    :param token:
    """
    current_key = decode_auth_token(token).encode("ascii", "ignore")
    existing_keys = db.session.query(APIKey).all()

    for key in existing_keys:
        db_key = key.key.encode("ascii", "ignore")
        if bcrypt.checkpw(current_key, db_key):
            return key

    abort(403, "The given authentication token is invalid")


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
