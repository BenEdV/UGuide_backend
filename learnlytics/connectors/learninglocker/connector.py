"""
This module connects to Learning Locker via API calls
"""

from base64 import b64encode
import logging
import requests

logger = logging.getLogger("learninglocker")


class LearningLockerConnector(object):
    """
    The connector to Remindo, and various calls
    """

    def __init__(self, api_base_url, username, password):
        self.api_base_url = api_base_url
        self.username = username
        self.password = password

        self._organisation_id = None
        self.headers = {
            'content-type': "application/json",
            'user-agent': 'Learnlytics Engine'
        }

    def get_client(self, params=None, json=None):
        """
        Create a request to the result/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of results
        """
        if params is None:
            params = {}
        return self._query('v2/client', json, params)

    def get_store(self, params=None, json=None, store_id=None):
        """
        Create a request to the result/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of results
        """
        if params is None:
            params = {}
        if store_id is None:
            url = 'v2/lrs'
        else:
            url = f"v2/lrs/{store_id}"
        return self._query(url, json, params)

    def post_client(self, params=None, json=None):
        """
        Create a request to the result/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of results
        """
        if params is None:
            params = {}
        return self._query('v2/client', json, params, method="post")

    def post_store(self, params=None, json=None):
        """
        Create a request to the result/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of results
        """
        if params is None:
            params = {}
        return self._query('v2/lrs', json, params, method="post")

    @property
    def organisation_id(self):
        if self._organisation_id is None:
            organisation = self._query("v2/organisation")
            self._organisation_id = organisation[0]["_id"]
        return self._organisation_id

    def _login(self):
        """
        Logs in with the credentials in the Connector settings and retrieves a JWT token to complete further calls
        """

        url = f"{self.api_base_url}/auth/jwt/password"
        logger.info(f"Logging into learning locker api")
        auth = b64encode(self.username.encode('ascii') + b":" + self.password.encode('ascii')).decode("ascii")
        login_headers = dict()
        login_headers["Authorization"] = "Basic " + auth
        response = requests.post(
            url=url,
            headers=login_headers,
            verify=False
        )

        self.headers["Authorization"] = "Bearer " + response.text

    request_methods = {
        "get": requests.get,
        "post": requests.post
    }

    def _query(self, action, json=None, params=None, method="get"):
        """
        Sends a query to Learning Locker
        """
        if "Authorization" not in self.headers:
            self._login()
        url = f"{self.api_base_url}/{action}"
        logger.info(f"Making {method} call to {url}")
        logger.debug(f"Params: {params}")

        response = self.request_methods[method](
            url=url,
            headers=self.headers,
            json=json,
            params=params,
            verify=False
        )

        print(f"The response code is {response.status_code}")
        result = response.json()
        if response.status_code != requests.codes.ok:
            print(result)

        logger.debug(f"Results: {result}")

        return result
