"""
This module connects to Learning Locker via API calls
"""

from base64 import b64encode
import requests


class LRSConnector(object):
    """
    The connector to Remindo, and various calls
    """

    def __init__(self, xapi_base_url, key, secret, api_version):
        self.xapi_base_url = xapi_base_url
        self.key = key
        self.secret = secret
        self.api_version = api_version

        auth = b64encode(key.encode('ascii') + b":" + secret.encode('ascii')).decode("ascii")
        self.headers = {
            'Authorization': f"Basic {auth}",
            'X-Experience-API-Version': api_version,
            'content-type': "application/json",
            'user-agent': 'Learnlytics Engine'
        }

    def get_statements(self, params=None, json=None):
        """
        Retrieves statements
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of statements
        """
        if params is None:
            params = {}
        return self._query('statements', json, params)

    def post_statements(self, params=None, json=None):
        """
        Posts new statements to the store
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of the new statements
        """
        if params is None:
            params = {}

        statement_ids = self._query('statements', json, params, method="post")
        if json is not None:
            for i, activity in enumerate(json):
                activity["id"] = statement_ids[i]
            return json
        else:
            return statement_ids

    request_methods = {
        "get": requests.get,
        "post": requests.post
    }

    def _query(self, action, json=None, params=None, method="get"):
        """
        Sends a query to Learning Locker
        """
        url = f"{self.xapi_base_url}/{action}"
        print(f"Making {method} call to {url}")

        response = self.request_methods[method](
            url=url,
            headers=self.headers,
            json=json,
            params=params,
            verify=False
        )

        result = response.json()
        print(f"result was {result}")
        return result
