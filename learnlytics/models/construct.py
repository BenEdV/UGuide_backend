"""
This module contains a classes with function for constructs
"""
from flask_restplus import abort
import copy

from learnlytics.authorization.manager import authorize
from learnlytics.extensions import db
from learnlytics.database.construct import Construct, ConstructModel, ConstructActivity, ConstructRelation
from learnlytics.database.studydata.activity import Activity


# pylint: disable=no-member
class Models(object):  # pylint: disable=no-init
    """
    The class contains methods for getting, adding, changing and removing models
    """

    @staticmethod
    def get_all_models(collection):
        result = []
        for model in collection.construct_models:
            result.append(Models.get_model(model.id))

        return result

    @staticmethod
    def get_model(id):
        """
        Gets the model with a given id
        :return: 404 or a dictionary containing all constructs
        """
        model = ConstructModel.get(id, required=True)
        return Models._model_dict(model)

    @staticmethod
    def _model_dict(model):
        model_dict = {
            "id": model.id,
            "name": model.name,
            "description": model.description,
            "method": model.method,
            "supported_construct_types": model.get_types(),
            "constructs": []
        }

        for construct in model.constructs:
            construct_dict = {
                "id": construct.id,
                "name": construct.name,
                "description": construct.description,
                "type": construct.type.name
            }
            model_dict["constructs"].append(construct_dict)

        return model_dict

    @staticmethod
    def add_model(collection, name, description, method):
        """
        Add a new model
        :return: 404 or the id of the newly created construct
        """
        new_model = ConstructModel(
            collection_id=collection.id,
            name=name,
            description=description,
            method=method
        )

        db.session.add(new_model)
        db.session.commit()

        return Models._model_dict(new_model)

    @staticmethod
    def update_model(model_id, data):
        """
        Edit the construct with a given id
        :return: 404 or True
        """
        model = ConstructModel.get(model_id, required=True)

        if "name" in data:
            model.name = data["name"]
        if "description" in data:
            model.description = data["description"]
        if "method" in data:
            model.method = data["method"]

        db.session.commit()

        return Models._model_dict(model)

    @staticmethod
    def delete_model(id):
        """
        Remove the construct with a given id
        :return: 404 or True
        """
        constructs = ConstructModel.get(id).constructs
        for construct in constructs:
            Constructs.delete_construct(construct.id)

        ConstructModel.remove_by_key(id)

    @staticmethod
    def add_construct_link(model_id, construct_id, type_id):
        """
        Creates a new link between a construct and a model
        :return: 404 or True
        """
        # TODO: Update scores as well
        model = ConstructModel.get(model_id)
        if model is None:
            abort(404, f"Model with id {model_id} could not be found")

        supported_types = [support_type["id"] for support_type in model.get_types()]
        if type_id not in supported_types:
            abort(404, f"Type with id {type_id} is not supported for model with id {model_id}")

        construct = Construct.get(construct_id)
        construct.model_id = model_id
        construct.type_id = type_id

    @staticmethod
    def delete_construct_link(model_id, construct_id):
        """
        Removes the link between a construct and a model
        :return: 404 or True
        """
        # TODO: Update scores as well
        construct = Construct.get(construct_id)
        construct.model_id = None

    @staticmethod
    def update_construct_link(model_id, construct_id, type_id):
        construct = Construct.get(construct_id)

        Models.delete_construct_link(model_id=construct.model_id, construct_id=construct_id)
        Models.add_construct_link(model_id=model_id, construct_id=construct_id, type_id=type_id)


# pylint: disable=no-member
class Constructs(object):  # pylint: disable=no-init
    """
    The class contains methods for getting, adding, changing and removing constructs
    """

    @staticmethod
    def get_construct(construct_id):
        """
        Gets a construct with the given construct_id.
        :param construct_id: id of the the construct to get
        :return: a json of the requested construct.
        """
        construct = Construct.get(construct_id, required=True)
        result_dic = Constructs._construct_dict(construct)

        return result_dic

    @staticmethod
    def _construct_dict(construct):
        construct_dict = {
            "id": construct.id,
            "name": construct.name,
            "description": construct.description,
            "type": construct.type.name,
            "model_id": construct.model_id,
            "properties": construct.properties,
            "head_constructs": ConstructModel._head_constructs_to_dict(construct.head_relations),
            "tail_constructs": ConstructModel._tail_constructs_to_dict(construct.tail_relations),
            "activities": []
        }

        return construct_dict

    @staticmethod
    def get_constructs(construct_ids):
        """
        Gets a list of all available constructs.
        :return: a list of json objects of all the available constructs.
        """
        constructs = Construct.query.filter(Construct.id.in_(construct_ids)).all()

        result = []
        construct_dicts = {}
        activities = set()

        for construct in constructs:
            construct_dict = Constructs._construct_dict(construct)
            result.append(construct_dict)
            activities.update(construct.activities)
            construct_dicts[construct.id] = construct_dict

        # activities
        activity_template_dicts = {}
        for activity in activities:
            if activity.visibility == "F" and \
                    not authorize(activity.collection, ["see_invisible_activities"], do_abort=False):
                continue
            activity_dict = {
                "title": activity.title,
                "id": activity.id,
                "type": activity.type.name
            }
            activity_template_dicts[activity.id] = activity_dict

        # construct values
        for construct_activity in ConstructActivity.query.filter(
                ConstructActivity.construct_id.in_(construct_ids)).all():
            if construct_activity.activity_id not in activity_template_dicts:
                continue
            activity_dict = copy.deepcopy(activity_template_dicts[construct_activity.activity_id])
            activity_dict["properties"] = construct_activity.properties
            activity_dict["relation_type"] = construct_activity.type.name
            construct_dicts[construct_activity.construct_id]["activities"].append(activity_dict)

        return result

    @staticmethod
    def get_collection_constructs(collection_id):
        """
        Gets all constructs
        :return: 404 or a dictionary containing the construct
        """

        all_construct_ids = db.session.query(Construct.id).join(ConstructModel, Construct.model).\
            filter(ConstructModel.collection_id == collection_id).\
            all()

        return Constructs.get_constructs(all_construct_ids)

    @staticmethod
    def add_construct(name, model, description, type_id, properties=None):
        """
        Add a new construct
        :return: 404 or the id of the newly created construct
        """
        if properties is None:
            properties = {}

        construct = Construct(
            name=name,
            description=description,
            properties=properties,
            type_id=type_id,
            model_id=model.id
        )

        db.session.add(construct)
        db.session.commit()

        return Constructs._construct_dict(construct)

    @staticmethod
    def update_construct(construct_id, data):
        """
        Edit the construct with a given id
        :return: 404 or True
        """
        construct = Construct.get(construct_id, required=True)

        if "name" in data:
            construct.name = data["name"]
        if "description" in data:
            construct.description = data["description"]
        if "properties" in data:
            construct.properties = data["properties"]
        if "model_id" in data and data["model_id"] != construct.model_id:
            type_id = data.get("type_id", construct.type_id)
            Models.update_construct_link(model_id=data["model_id"], construct_id=construct_id, type_id=type_id)
        elif "type_id" in data and data["type_id"] != construct.type_id:
            Models.update_construct_link(model_id=construct.model_id,
                                         construct_id=construct_id,
                                         type_id=data["type_id"])

        db.session.commit()

        return construct

    @staticmethod
    def delete_construct(id):
        """
        Remove the construct with a given id
        :return: 404 or True
        """
        activities = Construct.get(id).activities
        for activity in activities:
            ConstructActivityMappingModel.delete_map_construct(id, activity.id)

        Construct.remove_by_key(id)

    @staticmethod
    def get_mapping_suggestions(construct_id):
        construct = Construct.get(construct_id, required=True)
        keywords = construct.properties.get("keywords", [])
        if len(keywords) == 0:
            abort(409, "The construct does not have any keywords")

        activities = construct.model.collection.activities
        suggestions = []

        for activity in activities:
            occurrences = 0
            print(activity.id)
            for keyword in keywords:
                search_strings = []
                if activity.description is not None:
                    search_strings.append(activity.description)
                if activity.properties is not None:
                    if "body" in activity.properties and activity.properties["body"] is not None:
                        search_strings.append(activity.properties["body"])
                    if "prompt" in activity.properties and activity.properties["prompt"] is not None:
                        search_strings.append(activity.properties["prompt"])
                    if "answers" in activity.properties:
                        for answer in activity.properties["answers"]:
                            if "body" in answer:
                                search_strings.append(answer["body"])

                for search_string in search_strings:
                    print(search_string)
                    occurrences += search_string.count(keyword)

            if occurrences > 0:
                suggestions.append({"occ": occurrences, "id": activity.id, "title": activity.title})

        return suggestions


class ConstructMappingModel(object):

    @staticmethod
    def map_construct(head_construct_id, tail_construct_id, type_id, properties=None):
        head_construct = Construct.get(head_construct_id, required=True)
        tail_construct = Construct.get(tail_construct_id, required=True)

        if properties is None:
            properties = {}

        if head_construct.collection_id != tail_construct.collection_id:
            abort(409, "The given tail construct and head construct do not belong to the same collection")

        mapping = ConstructRelation(
            head_construct_id=head_construct_id,
            tail_construct_id=tail_construct_id,
            type_id=type_id,
            properties=properties
        )

        db.session.add(mapping)
        db.session.commit()

        return {
            "head_construct": ConstructModel._head_constructs_to_dict([mapping])[0],
            "tail_construct": ConstructModel._tail_constructs_to_dict([mapping])[0]
        }

    @staticmethod
    def update_map_construct(head_construct_id, tail_construct_id, data):
        mapping = ConstructRelation.query.filter(
            ConstructRelation.head_construct_id == head_construct_id,
            ConstructRelation.tail_construct_id == tail_construct_id
        ).one_or_none()

        if mapping is None:
            abort(404, "There is no existing mapping between the given construct and activity")

        if "type_id" in data:
            mapping.type_id = data["type_id"]
        if "properties" in data:
            mapping.properties = data["properties"]

        db.session.commit()

        return mapping

    @staticmethod
    def delete_map_construct(a_construct_id, b_construct_id):
        mapping = ConstructRelation.query.filter(
            ConstructRelation.head_construct_id == a_construct_id,
            ConstructRelation.tail_construct_id == b_construct_id
        ).one_or_none()

        if mapping is None:
            mapping = ConstructRelation.query.filter(
                ConstructRelation.head_construct_id == b_construct_id,
                ConstructRelation.tail_construct_id == a_construct_id
            ).one_or_none()

        if mapping is None:
            abort(404, "There is no existing mapping between the given construct and activity")

        db.session.delete(mapping)
        db.session.commit()

        return


class ConstructActivityMappingModel(object):

    @staticmethod
    def map_construct(construct_id, activity_id, type_id, properties=None):
        construct = Construct.get(construct_id, required=True)
        activity = Activity.get(activity_id, required=True)

        if properties is None:
            properties = {}

        if construct.collection_id != activity.collection_id:
            abort(409, "The given construct and activity do not belong to the same collection")

        mapping = ConstructActivity(
            construct_id=construct_id,
            activity_id=activity_id,
            type_id=type_id,
            properties=properties
        )

        db.session.add(mapping)
        db.session.commit()

        return {
            "activity": {
                "title": activity.title,
                "id": activity.id,
                "type": activity.type.name,
                "properties": properties,
                "relation_type": mapping.type.name
            },
            "construct": {
                "id": construct.id,
                "model_id": construct.model_id,
                "name": construct.name,
                "properties": construct.properties,
                "relation_properties": properties,
                "relation_type": mapping.type.name,
                "type": construct.type.name
            }
        }

    @staticmethod
    def update_map_construct(construct_id, activity_id, options):
        mapping = ConstructActivity.query.filter(
            ConstructActivity.construct_id == construct_id,
            ConstructActivity.activity_id == activity_id
        ).one_or_none()

        if mapping is None:
            abort(404, "There is no existing mapping between the given construct and activity")

        mapping.weight = options["weight"]

        db.session.commit()

        return

    @staticmethod
    def delete_map_construct(construct_id, activity_id):
        mapping = ConstructActivity.query.filter(
            ConstructActivity.construct_id == construct_id,
            ConstructActivity.activity_id == activity_id
        ).one_or_none()

        if mapping is None:
            abort(404, "There is no existing mapping between the given construct and activity")

        db.session.delete(mapping)
        db.session.commit()

        return
