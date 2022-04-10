"""
Contains the base class for unit tests using the database
"""
import datetime
import unittest
import json
import traceback

from config import get_config
from learnlytics import create_app
from learnlytics.extensions import db
from learnlytics.database.authorization import init_authorization_db
from learnlytics.database.connector.connector import Connector


class login:
    def __init__(self, client, username, password, idp="local"):
        """
        Used to simulate login
        :param client: the client application
        :param username: client username
        :param password: client password
        :param idp: user id
        :return: token
        """
        self.client = client
        self.username = username
        self.password = password
        self.idp = idp

    def __enter__(self):
        response = self.client.post('/currentuser/authentication', data=json.dumps(dict(
            username=self.username,
            password=self.password,
            idp=self.idp
        )), content_type='application/json', follow_redirects=True)
        data = json.loads(response.data)
        if "access_token" in data:
            jwt_token = data["access_token"]
            return UserClient(self.client, jwt_token)
        else:
            import learnlytics.database.studydata as md
            user = md.User.query.filter(md.User.id == self.username).one_or_none()
            user_count = db.session.query(md.User).count()
            if user:
                assert False, "Response code: {}, user does exist with name {}".format(
                    response.status_code, self.username)
            else:
                assert False, (
                    "Response code: {}, user does not exist with name {}. There are {} users in the"
                    " database").format(response.status_code, self.username, user_count)

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False

        return True


class api_login:
    def __init__(self, client, api_key):
        """
        Used to simulate login
        :param client: the client application
        :param username: client username
        :param password: client password
        :param idp: user id
        :return: token
        """
        self.client = client
        self.api_key = api_key

    def __enter__(self):
        response = self.client.post('/api/auth/', data=json.dumps(dict(
            api_key=self.api_key,
        )), content_type='application/json', follow_redirects=True)
        data = json.loads(response.data)
        if "auth_token" in data:
            jwt_token = data["auth_token"]
            return UserClient(self.client, jwt_token)
        else:
            assert False, "API key login failed. Response: {}".format(response.data)

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False

        return True


class UserClient:
    jwt_token = ""
    header = ""
    client = None

    def __init__(self, client, jwt_token):
        self.client = client
        self.jwt_token = jwt_token
        self.header = {'Authorization': 'JWT ' + self.jwt_token}

    def post(self, *args, **kwargs):
        kwargs['headers'] = self.header
        return self.client.post(*args, **kwargs)

    def get(self, *args, **kwargs):
        kwargs['headers'] = self.header
        return self.client.get(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs['headers'] = self.header
        return self.client.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['headers'] = self.header
        return self.client.delete(*args, **kwargs)


class TestLearnlytics(unittest.TestCase):
    """
    Contains the methods used to set up the meta-database
    """
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_obj=get_config("Testing"))
        cls.db = db

    def setUp(self):
        self.maxDiff = None
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.db.drop_all()
        self.db.create_all()

        init_authorization_db()
        # Add connectors
        connector = Connector(
            code="remindo",
            implementation="remindo",
            settings={
                "base_url": '',
                "uuid": '',
                "secret": ''
            })
        self.db.session.add(connector)

    def tearDown(self):
        # Removes the database
        self.db.session.remove()
        self.db.drop_all()

        self.app_context.pop()

    def assertStatusCode(self, response, expected_code):
        if response.status_code != expected_code:
            assert False, "Expected status code: {0}, found status code: {1}\nResponse data dump: {2}".\
                format(expected_code, response.status_code, response.data)

    def assertMessage(self, response, expected_message):
        data = json.loads(response.data)
        if data["message"] != expected_message:
            assert False, "Expected status message: {0}, found status message: {1}\nResponse data dump: {2}".\
                format(expected_message, data["message"], response.data)

    def assertDatetimeFormat(self, time, dateformat):
        date = datetime.datetime.strptime(time, dateformat)
        formatted_date_string = datetime.datetime.strftime(date, dateformat)
        self.assertEqual(time, formatted_date_string)
