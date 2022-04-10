from flask import request
from flask_restplus import Resource

from create_api import api_people_ns as ns
from learnlytics.api.models.authentication import authenticate
from learnlytics.api.models.authorization import authorize_gen_api
from learnlytics.api.models.person import PersonModel
from learnlytics.database.authorization.collection import Collection


@ns.route('/')
@ns.response(201, 'Created')
class AddPeopleResource(Resource):
    """
    The resource used to add people
    """
    model = PersonModel()

    def post(self):
        """
        Add people
        - __:param *request_data*__: Optional request_data for internal connector use.
        - __:return:__ True
        - JSON request data needs to be in the following layout:
        ```
        {
            "persons": [
                  {
                    "id": str,
                    "name": str,
                    "person_name": str,
                    "role": str,
                    "mail": str
                  },
                  {# more persons}
            ]
        }
        ```
        """
        key = authenticate()
        data = request.get_json()
        authorize_gen_api(key, Collection.get_root_collection(required=True).id, ["add_person"])

        return PersonModel.add_persons(data, source=key.requester), 201
