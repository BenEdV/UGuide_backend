# coding=utf-8
"""
This module contains all the endpoints for constructs
"""
from flask import request, jsonify
from flask_restplus import Resource, marshal, fields, abort
from io import StringIO

from create_api import modelns as ns
from learnlytics.authentication import auth_required
from learnlytics.authorization.manager import authorize
from learnlytics.connectors.csv_import.connect_construct_exam import connect_constructs_to_exam
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.construct.construct import ConstructModel, Construct
import learnlytics.database.studydata as md
from learnlytics.models.construct import Constructs, Models, ConstructMappingModel, ConstructActivityMappingModel
from learnlytics.resources.restplus_models.expect_models import post_model_fields, post_construct_fields


score_resource_fields = {
    "id": fields.Integer(),
    "first_name": fields.String(),
    "last_name": fields.String(),
    "score": fields.Float()
}

construct_resource_fields = {
    "id": fields.Integer(),
    "name": fields.String(),
    "description": fields.String()
}


@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ModelsResource(Resource):
    """
    This class is the resource endpoint for managing models.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all models.
        - __:return:__ True
        """
        collection = Collection.get(collection_id, required=True)
        authorize(collection, ["see_construct_models"])

        return Models.get_all_models(collection)

    @auth_required
    @ns.response(200, 'Success')
    @ns.expect(post_model_fields)
    def post(self, collection_id):  # pylint: disable=no-self-use
        """
        Adds a new construct model entity to the database.
        - __:body__: The title of the construct
        - __:return:__ True
        """
        collection = Collection.get(collection_id, required=True)
        authorize(collection, ["manage_construct_models"])

        data = request.get_json()

        if not isinstance(data, list):
            data = [data]

        models = []
        for model in data:
            model = Models.add_model(
                collection=collection,
                name=model["name"],
                description=model["description"],
                method=model["method"]
            )

            models.append(model)

        return models


@ns.route('/<int:model_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ModelResource(Resource):

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, model_id):  # pylint: disable=no-self-use
        """
        Gets the construct with a specific id
        - __:param *construct_id*: the unique id of the construct
        - __:return:__ construct with id = construct_id
        """
        model = ConstructModel.get(model_id, required=True)
        print(model.collection_id)
        authorize(model.collection, ["see_construct_models"])

        return Models.get_model(model_id)

    @auth_required
    @ns.response(200, 'Success')
    # @ns.expect(put_survey_construct_fields)
    def put(self, collection_id, model_id):  # pylint: disable=no-self-use
        """
        Changes data of an existing construct entity.
        - __:param *construct_id*__: The id of the construct
        - __:return__: True
        """

        model = ConstructModel.get(model_id, required=True)

        authorize(model.collection, ["manage_construct_models"])

        data = request.json
        return Models.update_model(model_id=model_id, data=data)

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id, model_id):  # pylint: disable=no-self-use
        """
        Deletes the construct
        - __:param *construct_id*: the unique id of the construct
        - __:return:__ True if it was deleted
        """
        model = ConstructModel.get(model_id, required=True)

        authorize(model.collection, ["manage_construct_models"])

        Models.delete_model(model_id)

        return None, 204


@ns.route('/constructs/')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConstructsResource(Resource):
    """
    This class is the resource endpoint for managing constructs.
    """

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        """
        Gets all constructs from all models of the collection.
        - __:return:__ True
        """
        collection = Collection.get(collection_id, required=True)

        authorize(collection, ["see_constructs"])

        return Constructs.get_collection_constructs(collection_id)

    @auth_required
    @ns.response(200, 'Success')
    @ns.expect(post_construct_fields)
    def post(self, collection_id):  # pylint: disable=no-self-use
        """
        Adds a new construct entity to the database.
        - __:body__: The title of the construct
        - __:return:__ True
        """
        data = request.get_json()

        if not isinstance(data, list):
            data = [data]

        constructs = []

        for construct in data:
            model = ConstructModel.get(construct["model_id"], required=True)
            if collection_id != model.collection_id:
                abort(400, "The given collection id does not match the collection id of the model")
            authorize(model.collection, ["manage_construct_models"])

            construct = Constructs.add_construct(
                name=construct["name"],
                model=model,
                description=construct["description"],
                type_id=construct["type_id"],
                properties=construct.get("properties", {})
            )

            constructs.append(construct)

        return constructs


@ns.route('/constructs/map_exam/<int:exam_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConstructsExamResource(Resource):
    """
    This class is the resource endpoint for managing exam constructs.
    """

    @auth_required
    @ns.response(200, 'Success')
    @ns.expect(post_construct_fields)
    def post(self, collection_id, exam_id):  # pylint: disable=no-self-use
        """
        Maps the constructs to the exam given
        - __:body__: The title of the construct
        - __:return:__ True
        """
        exam = md.Activity.get(exam_id, required=True)

        authorize(exam.collection, ["manage_construct_models"])
        if exam.collection_id != collection_id:
            abort(409, "The given exam does not belong to the given collection")
        files = request.files
        file = StringIO(files["file"].stream.read().decode("utf-8"))

        connect_constructs_to_exam(file, exam_id)

        return True, 201


@ns.route('/constructs/<int:construct_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConstructResource(Resource):

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, construct_id):  # pylint: disable=no-self-use
        """
        Gets the construct with a specific id
        - __:param *construct_id*: the unique id of the construct
        - __:return:__ construct with id = construct_id
        """
        construct = Construct.get(construct_id, required=True)

        authorize(construct.collection, ["see_constructs"])

        return Constructs.get_construct(construct_id)

    @auth_required
    @ns.response(200, 'Success')
    # @ns.expect(put_survey_construct_fields)
    def put(self, collection_id, construct_id):  # pylint: disable=no-self-use
        """
        Changes data of an existing construct entity.
        - __:param *construct_id*__: The id of the construct
        - __:return__: True
        """
        data = request.get_json()

        construct = Construct.get(construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        construct = Constructs.update_construct(construct_id, data)

        return marshal(construct, construct_resource_fields)

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id, construct_id):  # pylint: disable=no-self-use
        """
        Deletes the construct
        - __:param *construct_id*: the unique id of the construct
        - __:return:__ True if it was deleted
        """
        construct = Construct.get(construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        Constructs.delete_construct(construct_id)

        return None, 204


@ns.route('/constructs/<int:construct_id>/suggestions')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConstructSuggestionsResource(Resource):

    @auth_required
    @ns.response(200, 'Success')
    def get(self, collection_id, construct_id):  # pylint: disable=no-self-use
        """
        Gets the construct with a specific id
        - __:param *construct_id*: the unique id of the construct
        - __:return:__ construct with id = construct_id
        """
        construct = Construct.get(construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        return Constructs.get_mapping_suggestions(construct_id)


@ns.route('/constructs/<int:construct_id>/map_activity/<int:activity_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConstructActivityResource(Resource):

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id, construct_id, activity_id):  # pylint: disable=no-self-use
        """
        Attributes the given construct to the given activity
        - __:param *construct_id*: the unique id of the construct
        - __:param *activity_id*: the unique id of the activity
        - __:return:__ construct with id = construct_id
        """
        data = request.get_json()

        construct = Construct.get(construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        return ConstructActivityMappingModel.map_construct(construct_id,
                                                           activity_id,
                                                           data["type_id"],
                                                           data.get("properties", {}))

    @auth_required
    @ns.response(200, 'Success')
    def put(self, collection_id, construct_id, activity_id):  # pylint: disable=no-self-use
        """
        Updates the exisiting mapping between the given construct and the given activity
        - __:param *construct_id*: the unique id of the construct
        - __:param *activity_id*: the unique id of the activity
        - __:return:__ construct with id = construct_id
        """
        data = request.get_json()

        construct = Construct.get(construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        ConstructActivityMappingModel.update_map_construct(construct_id, activity_id, data)

        return None, 204

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id, construct_id, activity_id):  # pylint: disable=no-self-use
        """
        Updates the exisiting mapping between the given construct and the given activity
        - __:param *construct_id*: the unique id of the construct
        - __:param *activity_id*: the unique id of the activity
        - __:return:__ construct with id = construct_id
        """
        construct = Construct.get(construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        ConstructActivityMappingModel.delete_map_construct(construct_id, activity_id)

        return None, 204


@ns.route('/constructs/<int:head_construct_id>/map_construct/<int:tail_construct_id>')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Unauthorized')
@ns.response(404, 'Not Found')
class ConstructRelationResource(Resource):

    @auth_required
    @ns.response(200, 'Success')
    def post(self, collection_id, head_construct_id, tail_construct_id):  # pylint: disable=no-self-use
        """
        Attributes the given construct to the given activity
        - __:param *head_construct_id*: the unique id of the construct
        - __:param *tail_construct_id*: the unique id of the activity
        - __:return:__ construct with id = head_construct_id
        """
        data = request.get_json()

        construct = Construct.get(head_construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        return ConstructMappingModel.map_construct(head_construct_id,
                                                   tail_construct_id,
                                                   data["type_id"],
                                                   data.get("properties", {})), 201

    @auth_required
    @ns.response(200, 'Success')
    def put(self, collection_id, head_construct_id, tail_construct_id):  # pylint: disable=no-self-use
        """
        Updates the exisiting mapping between the given construct and the given activity
        - __:param *head_construct_id*: the unique id of the construct
        - __:param *tail_construct_id*: the unique id of the activity
        - __:return:__ construct with id = head_construct_id
        """
        data = request.get_json()

        construct = Construct.get(head_construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        ConstructMappingModel.update_map_construct(head_construct_id, tail_construct_id, data)

        return None, 204

    @auth_required
    @ns.response(200, 'Success')
    def delete(self, collection_id, head_construct_id, tail_construct_id):  # pylint: disable=no-self-use
        """
        Updates the exisiting mapping between the given construct and the given activity
        - __:param *head_construct_id*: the unique id of the construct
        - __:param *tail_construct_id*: the unique id of the activity
        - __:return:__ construct with id = head_construct_id
        """
        construct = Construct.get(head_construct_id, required=True)

        authorize(construct.collection, ["manage_construct_models"])

        ConstructMappingModel.delete_map_construct(head_construct_id, tail_construct_id)

        return None, 204
