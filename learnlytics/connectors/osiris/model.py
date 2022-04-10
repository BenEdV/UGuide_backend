
"""
This module contains the Osiris model
"""
import json
import requests

from learnlytics.authentication.util import current_identity
from learnlytics.database.authorization.user import UserToken
# from learnlytics.extensions import db


class OsirisModel(object):
    """
    Model containging info relevant for all Osiris calls
    """
    api_url = "https://api.prod.uu.connext.com/api/student/1.0.0"


class OsirisResultsModel(OsirisModel):
    """
    Model for calling Osiris for results
    """

    def get_results(self):
        """
        Uses access code to retrieve a token for authentication
        """
        user = current_identity()
        user_token = UserToken.query.filter(
            UserToken.user_id == user.id,
            UserToken.identity_provider == "UU").one_or_none()
        if user_token is None:
            return 204

        headers = {
            "Authorization": "Bearer " + user_token.token,
            "Content-type": "application/json"
        }

        response = requests.get(
            url=f"{OsirisModel.api_url}/{user.institution_id}/progress",
            headers=headers,
        )
        try:
            content = json.loads(response.content)
        except Exception:
            print(response)
            print(response.content)
            return 500
        return content
