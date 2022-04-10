"""
This module contains the model for activities
"""

import copy
import datetime
import os
import csv
import io
from flask import current_app
from flask_restplus import abort
from sqlalchemy import or_

from learnlytics.authentication import current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.api.models.result_model import Result as ApiResultModel
from learnlytics.extensions import db
from learnlytics.database.construct.construct import ConstructActivity
import learnlytics.database.studydata as md
from learnlytics.database.authorization.user import User
from learnlytics.util.datetime import strptime_frontend


delete_rules = {
    "exam_question": {
        "tail_activities": False,
        "head_activities": True
    }
}

update_visibility_rules = {
    "exam_question": {
        "tail_activities": False,
        "head_activities": True
    }
}


class ActivitiesModel(object):  # pylint: disable=no-init
    """
    Contains a methods which get available activities
    """

    @staticmethod
    def get_activity(activity_id):
        """
        Get the activity of the given collection with the given activity id
        :param activity_id: The id of the activity to get
        :return: 404 or a dictionary containing the activity data
        """
        # ids = [activity_id]
        # activity = md.Activity.get(activity_id, required=True)
        # for tail_activity in activity.tail_activities:
        #     ids.append(tail_activity.id)
        # return ActivitiesModel.get_activities(ids)[0]
        return ActivitiesModel.get_activities([activity_id])[0]

    @staticmethod
    def get_collection_activities(collection, limit=None, type_name=None):
        """
        """
        activity_ids = []
        if type_name is not None:
            activity_type = md.ActivityType.query.filter(md.ActivityType.name == type_name).one()
            activities = collection.activities.\
                filter(md.Activity.type_id == activity_type.id).order_by(md.Activity.date_added).limit(limit)
        else:
            activities = collection.activities.order_by(md.Activity.date_added).limit(limit)

        can_see_invisible = authorize(collection, ["see_invisible_activities"], do_abort=False)

        for activity in activities:
            if can_see_invisible or activity.visibility == "T":
                activity_ids.append(activity.id)
        return ActivitiesModel.get_activities(activity_ids)

    @staticmethod
    def get_all_activities(user_id, type_name=None):
        """
        Get all activities that the given user has access to
        """
        user = User.get(user_id, required=True)
        collections = user.collections_with_permissions(["see_activities"])

        activities = []

        for collection in collections:
            collection_activities = ActivitiesModel.get_collection_activities(collection, limit=5, type_name=type_name)
            for activity_dict in collection_activities:
                activity_dict["collection_id"] = collection.id
            activities.extend(collection_activities)

        return activities

    @staticmethod
    def get_activities(activity_ids):
        """
        Returns a list of activities for the ids provided
        """
        res = []

        # !!!!!!!
        # Database calls
        # !!!!!!!

        # activities
        activities = md.Activity.query.filter(md.Activity.id.in_(activity_ids)).all()
        if activities == []:
            return []
        collection = activities[0].collection

        can_see_invisible = authorize(collection, ["see_invisible_activities"], do_abort=False)

        for activity in activities:
            if activity.collection != collection:
                abort(409, "Request contains activities from different collections")
            if activity.visibility == "F" and not can_see_invisible:
                authorize(activity.collection, ["see_invisible_activities"])

        # constructs
        construct_ids = []
        construct_template_dicts = {}
        for construct_model in collection.construct_models:
            for construct in construct_model.constructs:
                construct_ids.append(construct.id)
                construct_dict = {
                    "name": construct.name,
                    "id": construct.id,
                    "type": construct.type.name,
                    "model_id": construct.model_id,
                    "properties": construct.properties
                }
                construct_template_dicts[construct.id] = construct_dict

        # !!!!!!!
        # Creating dictionary
        # !!!!!!!
        activity_dicts = {}
        activity_dicts_for_remote = {}
        for activity in activities:
            activity_dict = {
                "id": activity.id,
                "title": activity.title,
                "type": activity.type.name,
                "visible": activity.visibility,
                "description": activity.description,
                "properties": activity.properties,
                "date_added": activity.date_added,
                "start_time": activity.start_time,
                "end_time": activity.end_time,
                "results": [],
                "constructs": [],
                "tail_activities": [],
                "head_activities": [],
                "attachments": [],
                "my_results": []
            }

            activity_dicts[activity.id] = activity_dict
            if activity.lrs_object_id is not None:
                activity_dicts_for_remote[activity.lrs_object_id] = activity_dict
            res.append(activity_dict)

        for attachment in md.ActivityAttachment.query.filter(md.ActivityAttachment.activity_id.in_(activity_ids)).all():
            activity_dicts[attachment.activity_id]["attachments"].append({
                "id": str(attachment.uuid),
                "name": attachment.name,
                "extension": attachment.extension
            })

        # construct values
        for construct_activity in ConstructActivity.query.filter(
                ConstructActivity.activity_id.in_(activity_ids)).all():
            construct_dict = copy.deepcopy(construct_template_dicts[construct_activity.construct_id])
            construct_dict["relation_properties"] = construct_activity.properties
            construct_dict["relation_type"] = construct_activity.type.name
            activity_dicts[construct_activity.activity_id]["constructs"].append(construct_dict)

        # related activities
        for activity_relation in md.ActivityRelation.query.filter(
                or_(
                    md.ActivityRelation.head_activity_id.in_(activity_ids),
                    md.ActivityRelation.tail_activity_id.in_(activity_ids)
                )).all():
            head_related_dict = {
                "id": activity_relation.head_activity_id,
                "relation_type": activity_relation.type.name,
                "relation_properties": activity_relation.properties
            }
            tail_related_dict = {
                "id": activity_relation.tail_activity_id,
                "relation_type": activity_relation.type.name,
                "relation_properties": activity_relation.properties
            }
            if activity_relation.tail_activity_id in activity_dicts:
                activity_dicts[activity_relation.tail_activity_id]["head_activities"].append(head_related_dict)
            if activity_relation.head_activity_id in activity_dicts:
                activity_dicts[activity_relation.head_activity_id]["tail_activities"].append(tail_related_dict)

        # results
        lrs_connector = collection.main_lrs_connector()
        show_user_id = False
        if authorize(collection, ["see_user_results"], do_abort=False):
            show_user_id = True
            persons = md.Person.query.filter(md.Person.user_id.in_(collection.all_user_ids)).all()
            user_id_for_actor = {}
            for user in collection.all_users:
                user_id_for_actor[str(user.actor)] = user.id
            for person in persons:
                user_id_for_actor[str(person.lrs_actor)] = person.user_id

        if authorize(collection, ["see_anonymized_user_results"], do_abort=False):
            for activity_id in activity_dicts:
                activity_dicts[activity_id]["results"] = []
            # Get all results
            params = {
                "statement.object.id": {"$in": list(activity_dicts_for_remote.keys())}
            }

            for statement in lrs_connector.model.get_statements(params):
                if "result" not in statement:
                    continue

                object_id = statement["object"]["id"]

                if "success" not in statement["result"] and "score" in statement["result"]:
                    is_max_score = statement["result"]["score"]["max"] == statement["result"]["score"]["raw"]
                    statement["result"]["success"] = is_max_score

                result = {
                    "id": statement["id"],
                    "verb": statement["verb"],
                    "result": statement["result"],
                    "timestamp": statement["timestamp"]
                }

                if show_user_id:
                    actor = str(statement["actor"].get("account", None))
                    result["user_id"] = user_id_for_actor.get(actor, -1)

                activity_dicts_for_remote[object_id]["results"].append(result)

        if authorize(collection, ["see_own_results"], do_abort=False):
            # Get user's own results
            actors = [current_identity().actor]

            for person in current_identity().persons:
                actors.append(person.get_lrs_actor())

            params = {
                "statement.actor.account": {"$in": actors},
                "statement.object.id": {"$in": list(activity_dicts_for_remote.keys())}
            }

            for statement in lrs_connector.model.get_statements(params):
                if "result" not in statement:
                    continue
                object_id = statement["object"]["id"]

                result = {
                    "id": statement["id"],
                    "verb": statement["verb"],
                    "result": statement["result"],
                    "timestamp": statement["timestamp"],
                }
                if "context" in statement:
                    result["context"] = statement["context"]

                activity_dicts_for_remote[object_id]["my_results"].append(result)

        res.sort(key=lambda q: q["id"])

        return res

    @staticmethod
    def new_activity(collection_id, activity_data, files=None):
        activity = md.Activity(
            title=activity_data["title"],
            description=activity_data.get("description", ''),
            start_time=activity_data.get("start_time", None),
            end_time=activity_data.get("end_time", None),
            remote_id="local",
            type_id=activity_data.get("type_id", None),
            visibility=activity_data["visibility"],
            collection_id=collection_id,
            properties=activity_data.get("properties", {})
        )

        db.session.add(activity)
        db.session.commit()

        if files:
            ActivitiesModel.add_attachments(activity.id, files)

        return ActivitiesModel.get_activity(activity.id)

    @staticmethod
    def update_activity(activity_id, activity_data):
        activity = md.Activity.get(activity_id)

        if "title" in activity_data:
            activity.title = activity_data["title"]
        if "description" in activity_data:
            activity.description = activity_data["description"]
        if "start_time" in activity_data:
            activity.start_time = activity_data["start_time"]
        if "end_time" in activity_data:
            activity.end_time = activity_data["end_time"]
        if "visibility" in activity_data:
            activity.visibility = activity_data["visibility"]
            for head_relation in activity.head_relations:
                type_name = head_relation.type.name
                if type_name in delete_rules:
                    if update_visibility_rules[type_name]["head_activities"]:
                        head_relation.head_activity.visibility = activity_data["visibility"]

            for tail_relation in activity.tail_relations:
                type_name = tail_relation.type.name
                if type_name in delete_rules:
                    if update_visibility_rules[type_name]["tail_activities"]:
                        tail_relation.tail_activity.visibility = activity_data["visibility"]

        if "properties" in activity_data:
            activity.properties = activity_data["properties"]
        if "type_id" in activity_data:
            activity.type_id = activity_data["type_id"]

        db.session.commit()

        return ActivitiesModel.get_activity(activity.id)

    @staticmethod
    def delete_activity(activity_id):
        activity = md.Activity.get(activity_id, required=True)

        for attachment in activity.attachments:
            ActivitiesModel.delete_attachment(attachment)

        for head_relation in activity.head_relations:
            type_name = head_relation.type.name
            if type_name in delete_rules:
                if delete_rules[type_name]["head_activities"]:
                    db.session.delete(head_relation)
                    ActivitiesModel.delete_activity(head_relation.head_activity_id)

        for tail_relation in activity.tail_relations:
            type_name = tail_relation.type.name
            if type_name in delete_rules:
                if delete_rules[type_name]["tail_activities"]:
                    db.session.delete(tail_relation)
                    ActivitiesModel.delete_activity(tail_relation.tail_activity_id)

        db.session.delete(activity)
        db.session.commit()

    @staticmethod
    def connect_activities(head_activity_id, tail_activity_id, type_id, properties):
        head_activity = md.Activity.get(head_activity_id, required=True)
        tail_activity = md.Activity.get(tail_activity_id, required=True)

        if head_activity.collection_id != tail_activity.collection_id:
            abort(409, "The two given activities do not belong to the same collection")

        relation = md.ActivityRelation(
            tail_activity_id=tail_activity_id,
            head_activity_id=head_activity_id,
            type_id=type_id,
            properties=properties
        )

        db.session.add(relation)
        db.session.commit()

        return {
            "head_activity": ActivitiesModel._head_activities_to_dict([relation])[0],
            "tail_activity": ActivitiesModel._tail_activities_to_dict([relation])[0]
        }

    @staticmethod
    def update_activity_connection(head_activity_id, tail_activity_id, type_id, properties):
        relation = md.ActivityRelation.query.filter(
            md.ActivityRelation.tail_activity_id == tail_activity_id,
            md.ActivityRelation.head_activity_id == head_activity_id).one_or_none()

        if relation is None:
            abort(409, "The two given activities do not have a relation")

        if type_id is not None:
            relation.type_id = type_id
        if properties is not None:
            relation.properties = properties

        db.session.commit()

        return {
            "head_activity": ActivitiesModel._head_activities_to_dict([relation])[0],
            "tail_activity": ActivitiesModel._tail_activities_to_dict([relation])[0]
        }

    @staticmethod
    def delete_activity_connection(head_activity_id, tail_activity_id):
        relation = md.ActivityRelation.query.filter(
            md.ActivityRelation.tail_activity_id == tail_activity_id,
            md.ActivityRelation.head_activity_id == head_activity_id).one_or_none()

        if relation is None:
            abort(409, "The two given activities do not have a relation")

        db.session.delete(relation)
        db.session.commit()

    @staticmethod
    def _head_activities_to_dict(head_relations):
        result = []
        for relation in head_relations:
            relation_dict = {
                "id": relation.head_activity_id,
                "relation_type": relation.type.name,
                "relation_properties": relation.properties
            }
            result.append(relation_dict)

        return result

    @staticmethod
    def _tail_activities_to_dict(tail_activities):
        result = []
        for relation in tail_activities:
            relation_dict = {
                "id": relation.tail_activity_id,
                "relation_type": relation.type.name,
                "relation_properties": relation.properties
            }
            result.append(relation_dict)

        return result

    @staticmethod
    def mark_as_completed(collection, activity_id, context):
        activity = md.Activity.get(activity_id, required=True)
        if activity.type.name == "survey":
            completed_statements, is_completed = ActivitiesModel.check_completed(collection, activity)
            if not is_completed:
                abort(409, "Not all the required questions of the survey were completed")

            ApiResultModel.calculate_construct_scores(
                collection=collection,
                data=completed_statements,
                activity_ids=[statement[0] for statement in completed_statements],
                user_ids=[current_identity().id]
            )
        statement = ActivitiesModel.__mark_activity(
            collection,
            activity_id,
            "http://adlnet.gov/expapi/verbs/completed",
            context
        )

        lrs_connector = collection.main_lrs_connector()
        result = lrs_connector.model.post_statements([statement])

        return result[0]

    @staticmethod
    def mark_as_started(collection, activity_id, context):
        """
        Marks the survey as being started again this resets the construct scores to 0
        """
        activity = md.Activity.get(activity_id, required=True)
        statement = ActivitiesModel.__mark_activity(
            collection,
            activity_id,
            "http://adlnet.gov/expapi/verbs/initialized",
            context)

        result_data = [(activity_id, current_identity().id, statement)]

        result = ApiResultModel.add_results(result_data, collection.id)

        return result[0]

    @staticmethod
    def __mark_activity(collection, activity_id, verb, context):
        activity = md.Activity.get(activity_id, required=True)
        print(current_identity().actor)
        statement = {
            "actor": {
                "account": current_identity().actor,
                "objectType": "Agent"
            },
            "verb": {
                "id": verb
            },
            "object": {
                "id": activity.lrs_object_id,
                "objectType": "Activity"
            },
            "result": {
                "success": True,
            },
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }

        if context is not None:
            statement["context"] = context

        return statement

    @staticmethod
    def check_completed(collection, activity):
        lrs_connector = collection.main_lrs_connector()
        result_data = []
        completed = True
        if activity.type.name == "survey":
            for child_activity in activity.head_activities:
                if not child_activity.type.name.startswith("question"):
                    continue

                most_recent_exam_time = ActivitiesModel.__most_recent_exam_time(lrs_connector, activity, current_identity().actor)
                params = {
                    "statement.actor.account": current_identity().actor,
                    "statement.object.id": child_activity.lrs_object_id
                }
                if most_recent_exam_time is not None:
                    params["timestamp"] = {"$gt": most_recent_exam_time}
                existing_results = lrs_connector.model.get_unprocessed_statements(params)

                print("Activity:")
                print(child_activity)
                print("------------------------------------------------------")

                print("Most recent exam time:")
                print(most_recent_exam_time)
                print("------------------------------------------------------")

                print("Existing results:")
                print(existing_results)
                print("------------------------------------------------------")

                answer_found = False
                for existing_result in existing_results:
                    if existing_result["verb"]["id"] == "http://adlnet.gov/expapi/verbs/answered":
                        result_data.append((child_activity.id, current_identity().id, existing_result))
                        answer_found = True
                        break # only use the latest (first) result

                if not answer_found and child_activity.properties["required"]:
                    completed = False

        return result_data, completed

    @staticmethod
    def give_reponse(collection, activity_responses):
        statements = []
        lrs_connector = collection.main_lrs_connector()
        activity_lrs_dict = {}

        for response in activity_responses:
            activity = md.Activity.get(response["activity_id"], required=True)
            activity_lrs_dict[activity.lrs_object_id] = activity.id
            exam_activity = activity.tail_activities[0]
            most_recent_exam_time = ActivitiesModel.__most_recent_exam_time(lrs_connector, exam_activity, current_identity().actor)

            if activity.collection != collection:
                abort(409, "Request contains activities from different collections")
            params = {
                "statement.actor.account": current_identity().actor,
                "statement.object.id": activity.lrs_object_id
            }
            if most_recent_exam_time is not None:
                params["timestamp"] = {"$gt": most_recent_exam_time}
            existing_results = lrs_connector.model.get_statements(params)
            for existing_result in existing_results:
                if existing_result["verb"]["id"] == "http://adlnet.gov/expapi/verbs/answered":
                    id_to_void = existing_result["id"]
                    void_statement = ActivitiesModel.__void_statement(id_to_void)
                    statements.append(void_statement)

            statement = ActivitiesModel.__question_statement(
                activity.lrs_object_id,
                response["answer_id"],
                response["timestamp"]
            )
            statements.append(statement)

        statement_results = lrs_connector.model.post_statements(statements)

        result = []
        for statement in statement_results:
            if statement["verb"]["id"] == "http://adlnet.gov/expapi/verbs/voided":
                continue
            print(statement)

            result.append({
                "id": statement["id"],
                "verb": statement["verb"],
                "result": statement["result"],
                "timestamp": statement["timestamp"]
            })

        return result

    @staticmethod
    def __most_recent_exam_time(lrs_connector, activity, account=None):
        most_recent_exam_time = None
        params = {
            "statement.object.id": activity.lrs_object_id
        }

        if account is not None:
            params["statement.actor.account"] = account

        existing_exam_results = lrs_connector.model.get_statements(params)
        for existing_result in existing_exam_results:
            if existing_result["verb"]["id"] == "http://adlnet.gov/expapi/verbs/completed":
                exam_time = strptime_frontend(existing_result["timestamp"])
                if most_recent_exam_time is None or exam_time > most_recent_exam_time:
                    most_recent_exam_time = exam_time

        return most_recent_exam_time

    @staticmethod
    def __question_statement(lrs_object_id, response, timestamp):
        return {
            "actor": {
                "account": current_identity().actor,
                "objectType": "Agent"
            },
            "verb": {
                "id": "http://adlnet.gov/expapi/verbs/answered"
            },
            "object": {
                "id": lrs_object_id,
                "objectType": "Activity"
            },
            "result": {
                "response": str(response)
            },
            "timestamp": timestamp
        }

    @staticmethod
    def void_statement(collection, activity_id, statement_id):
        activity = md.Activity.get(activity_id, required=True)
        lrs_connector = collection.main_lrs_connector()
        params = {
            "statement.object.id": activity.lrs_object_id,
            "statement.id": statement_id
        }
        existing_results = lrs_connector.model.get_statements(params)
        if len(existing_results) == 0:
            abort(409, "The statement does not belong to the activity")
        else:
            for existing_result in existing_results:
                statement = ActivitiesModel.__void_statement(statement_id)
                lrs_connector.model.post_statements([statement])

    @staticmethod
    def __void_statement(statement_id):
        return {
            "actor": {
                "account": current_identity().actor,
                "objectType": "Agent"
            },
            "verb": {
                "id": "http://adlnet.gov/expapi/verbs/voided"
            },
            "object": {
                "objectType": "StatementRef",
                "id": statement_id
            }
        }

    @staticmethod
    def _attachment_dict(attachment):
        attachment_dict = {
            "id": attachment.uuid,
            "name": attachment.name,
            "extension": attachment.extension
        }

        return attachment_dict

    @staticmethod
    def add_attachments(activity_id, files):
        result = []

        for file in files:
            name = file.filename.rsplit('.', 1)[0]
            extension = file.filename.rsplit('.', 1)[1]
            attachment = md.ActivityAttachment(
                name=name,
                extension=extension,
                activity_id=activity_id
            )
            db.session.add(attachment)
            db.session.flush()
            result.append(ActivitiesModel._attachment_dict(attachment))

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], attachment.uuid))

        return result

    @staticmethod
    def add_attachment_from_content(activity_id, content, filename):
        name = filename.rsplit('.', 1)[0]
        extension = filename.rsplit('.', 1)[1]
        attachment = md.ActivityAttachment(
            name=name,
            extension=extension,
            activity_id=activity_id
        )
        db.session.add(attachment)
        db.session.flush()
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], attachment.uuid), "wb") as file:
            file.write(content)

        return attachment

    @staticmethod
    def delete_attachment(attachment):
        os.remove(current_app.config['UPLOAD_FOLDER'] + "/" + str(attachment.uuid))

        db.session.delete(attachment)
        db.session.commit()

        return 204

    @staticmethod
    def get_user_statements(collection, users, out_format="json"):
        # Get user's own results
        lrs_connector = collection.main_lrs_connector()

        actors = [user.actor for user in users]

        for user in users:
            for person in user.persons:
                actors.append(person.get_lrs_actor())

        params = {
            "statement.actor.account": {"$in": actors},
        }

        statements = lrs_connector.model.get_statements(params)
        if out_format == "json":
            return statements
        else:
            output = io.StringIO()
            writer = csv.writer(output)
            header = ['user_id', 'verb_id', 'object_id', 'response']
            writer.writerow(header)

            for statement in statements:
                if "result" not in statement:
                    continue
                row = [
                    str(statement["actor"]["account"]["name"]),
                    str(statement["verb"]["id"]),
                    str(statement["object"]["id"]),
                    str(statement["result"].get("response", "")),
                ]
                writer.writerow(row)

            output.seek(0)
            return output

    @staticmethod
    def export_activity_responses(collection, parent_activity_id, users):
        lrs_connector = collection.main_lrs_connector()

        parent = md.Activity.get(parent_activity_id)
        user_results = {}
        for user in users: # create a row for every user
            user_results[user.id] = {}

        actors = [user.actor for user in users]
        questions = []
        for activity in parent.head_activities:
            if activity.type.name.startswith("question"):
                questions.append(activity)

        for activity in questions:
            params = {
                "statement.actor.account": {"$in": actors},
                "statement.object.id": activity.lrs_object_id
            }

            statements = lrs_connector.model.get_statements(params) # find all user results for this question

            for statement in statements:
                statement_user_id = int(statement["actor"]["account"]["name"])

                if "result" not in statement or activity.id in user_results[statement_user_id]:
                    continue # continue if there is no result or a later result has already been found

                user_results[statement_user_id][activity.id] = statement["result"].get("response", "")

        rows = [["user_id"]]
        for activity in questions:
            rows[0].append(activity.title)

        for user in users:
            row = [user.id]
            for activity in questions:
                if activity.id in user_results[user.id]:
                    row.append(user_results[user.id][activity.id])
                else:
                    row.append("")
            rows.append(row)

        output = io.StringIO()
        writer = csv.writer(output)
        for row in rows:
            writer.writerow(row)

        output.seek(0)
        return output
