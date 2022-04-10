"""
This module connects to Remindo via API calls
"""

import logging
import requests

import learnlytics.connectors.remindo.utils as utils

logger = logging.getLogger("remindo")


class RemindoConnector(object):
    """
    The connector to Remindo, and various calls
    """

    def __init__(self, base_url, uuid, secret):
        self.base_url = base_url
        self.uuid = uuid
        self.secret = secret

    headers = {
        'content-type': 'application/json',
        'user-agent': 'Learnlytics Engine',
        'x-request': 'JSON',
    }

    def result_list(self, params=None):
        """
        Create a request to the result/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of results
        """
        if params is None:
            params = {}
        return self._query('result/list', params)

    def itemresult_list(self, params=None):
        """
        Create a request to the itemresult/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of question/item results
        """
        if params is None:
            params = {}
        return self._query('itemresult/list', params)

    def itemresult_stats(self, params=None):
        """
        Create a request to the itemresult/stats API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of question/item results statistics
        """
        if params is None:
            params = {}
        return self._query('itemresult/stats', params)

    def recipe_list(self, params=None, print_result=False):
        """
        Create a request to the recipe/list API of Remindo and send the request to Remindo
        Requires a recipe_id
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of recipes
        """
        if params is None:
            params = {}
        return self._query('recipe/list', params)

    def study_list(self, params=None):
        """
        Create a request to the study/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of studies
        """
        if params is None:
            params = {}
        return self._query('study/list', params)

    def user_get(self, params=None):
        """
        Create a request to the user/get API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing one user
        """
        if params is None:
            params = {}
        return self._query('user/get', params)

    def user_list(self, params=None):
        """
        Create a request to the user/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of users
        """
        if params is None:
            params = {}
        return self._query('user/list', params)

    def item_get(self, params=None):
        """
        Create a request to the item/get API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of users
        """
        if params is None:
            params = {}
        return self._query('item/get', params)

    def item_view(self, params=None):
        """
        Create a request to the item/view API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of users
        """
        if params is None:
            params = {}
        return self._query('item/view', params)

    def moment_list(self, params=None, print_result=False):
        """
        Create a request to the moment/list API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of students assigned to a test at this point in time
        """
        if params is None:
            params = {}
        return self._query('moment/list', params)

    def moment_list_candidates(self, params=None):
        """
        Create a request to the moment/list_candidates API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of students assigned to a test at this point in time
        """
        if params is None:
            params = {}
        return self._query('moment/list_candidates', params)

    def moment_results(self, params=None):
        """
        Create a request to the moment/list_candidates API of Remindo and send the request to Remindo
        :param params: The parameters to be sent with the request
        :return: The response to the API request, containing a list of students assigned to a test at this point in time
        """
        if params is None:
            params = {}
        return self._query('moment/results', params)

    def hello_world(self, params=None):
        """
        The testcall to Remindo
        :param params: None
        :return: Hello World
        """
        if params is None:
            params = {}
        return self._query('remote_api/hello_world', params)

    def _query(self, action, params=None):
        """
        Sends a query to Remindo
        :param action: the Remindo action
        :param params:  A dict of params to the Remindo action, can be omitted.
        :param print_result: Boolean, debug feature to see what is being returned by remindo
        :return: a requests response
        """
        url = '{}/{}'.format(self.base_url, action)
        ip_addr = requests.get('http://ip.42.pl/raw').text
        logger.info(f"Making call to {url}, with uuid: {self.uuid}")
        logger.debug(f"Params:\n{utils.json.dumps(params, indent=4)}")
        data = utils.create_package(params, str(self.uuid), str(self.secret), str(ip_addr))
        response = requests.post(
            url=url,
            headers=self.headers,
            data=utils.json_dumps(data),
        )

        result = utils.json.loads(response.json()['payload'])
        logger.debug(f"Results:\n{utils.json.dumps(result, indent=4)}")

        if 'success' not in result:
            raise Exception(result)
        elif not result['success']:
            if result["error"] == "No results found":
                return {}
            raise Exception("RemindoError: %s" % result['error'])
        else:
            if not utils.verify_signature(response.json(), str(self.secret), url, response.json()['signature']):
                raise Exception("Remindo signature does not match payload")

        return result
