"""
This module contains a classes with function for retrieving concepts and mapping concepts on tests
"""

import json
import csv
import io
from datetime import datetime
from sqlalchemy import asc

from learnlytics.extensions import db
import learnlytics.database.studydata as md
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.learnlyticslogging.statelog import EventLog, EventState, EventSubject, EventType
from learnlytics.database.learnlyticslogging.requestlog import RequestLog
from learnlytics.util.datetime import strptime_frontend
from learnlytics.models.scores import ScoresModel
from learnlytics.database.construct import Construct


# pylint: disable=no-member
class LoggingState(object):  # pylint: disable=no-init
    """
    The class contains methods called by the logging resource.
    """

    @staticmethod
    def add_state(user, session_id, data):  # pylint: disable=too-many-arguments
        """
        Adds a new entry state change to the logging table.
        :param user: The current user
        :param from_state: The state the user came from
        :param to_state: The state the user is going to
        :param timestamp: The time at which the redirection occurred
        :return: 404 or nothing
        """
        timestamp = strptime_frontend(data["timestamp"])

        parameters = json.dumps(data.get("parameters", None))
        details = json.dumps(data.get("details", None))
        subsession = json.dumps(data.get("subsession", None))

        state = EventState.query.filter(EventState.name == data["url"]).one_or_none()
        if state is None:
            state = EventState(name=data["url"])
            db.session.add(state)

        subject = EventSubject.query.filter(EventSubject.name == data["subject"]).one_or_none()
        if subject is None:
            subject = EventSubject(name=data["subject"])
            db.session.add(subject)

        _type = EventType.query.filter(EventType.name == data["event"]).one_or_none()
        if _type is None:
            _type = EventType(name=data["event"])
            db.session.add(_type)

        log = EventLog(
            user_id=user.id,
            session_id=session_id,
            state=state,
            subject=subject,
            e_type=_type,
            details=details,
            parameters=parameters,
            timestamp=timestamp,
            subsession=subsession)
        db.session.add(log)
        db.session.commit()

    @staticmethod
    def request_log_report(user_ids):

        requests = RequestLog.query.filter(RequestLog.user_id.in_(user_ids)).all()

        output = io.StringIO()
        writer = csv.writer(output)
        header = ['user_id', 'timestamp', 'request_path', 'request_method']
        writer.writerow(header)

        for request in requests:
            row = [
                str(request.user_id),
                str(request.time),
                str(request.request_path),
                str(request.request_method)
            ]

            writer.writerow(row)

        output.seek(0)
        return output

    @staticmethod
    def state_log_report(user_ids):

        requests = EventLog.query.filter(EventLog.user_id.in_(user_ids)).order_by(EventLog.timestamp).all()

        output = io.StringIO()
        writer = csv.writer(output)
        header = ['user_id', 'session_id', 'timestamp', 'details', 'parameters', 'state', 'subject', 'type']
        writer.writerow(header)

        for request in requests:
            row = [
                str(request.user_id),
                str(request.session_id),
                str(request.timestamp),
                str(request.details),
                str(request.parameters),
                str(request.state.name),
                str(request.subject.name),
                str(request.e_type.name)
            ]

            writer.writerow(row)

        output.seek(0)
        return output

    @staticmethod
    def thermos_log_report(start_time, end_time):
        _activityHeaders = {
            "397": "ProgressAnxietyAct1",
            "325": "FinishedQuestionnaire",
            "410": "ProgressAnxietyAct2",
            "414": "ProgressAnxietyAct3",
            "418": "ProgressAnxietyPrepare",
            "430": "ProgressAnxietyReflect",
            "440": "ProgressFailure avoidanceAct1",
            "449": "ProgressFailure avoidanceAct2",
            "458": "ProgressFailure avoidanceAct3",
            "467": "ProgressFailure avoidancePrepare",
            "479": "ProgressFailure avoidanceReflect",
            "489": "ProgressUncertain controlAct1",
            "497": "ProgressUncertain controlAct2",
            "562": "ProgressSelf-sabotageReflect",
            "504": "ProgressUncertain controlAct3",
            "513": "ProgressUncertain controlPrepare",
            "525": "ProgressUncertain controlReflect",
            "534": "ProgressSelf-sabotageAct1",
            "539": "ProgressSelf-sabotageAct2",
            "544": "ProgressSelf-sabotageAct3",
            "550": "ProgressSelf-sabotagePrepare",
            "572": "ProgressDisengagementAct1",
            "585": "ProgressDisengagementAct2",
            "613": "ProgressDisengagementAct3",
            "618": "ProgressDisengagementPrepare",
            "630": "ProgressDisengagementReflect",
            "640": "ProgressSelf beliefAct1",
            "647": "ProgressSelf beliefAct2",
            "654": "ProgressSelf beliefAct3",
            "669": "ProgressSelf beliefPrepare",
            "681": "ProgressSelf beliefReflect",
            "691": "ProgressLearning focusAct1",
            "707": "ProgressLearning focusAct2",
            "717": "ProgressLearning focusAct3",
            "726": "ProgressLearning focusPrepare",
            "738": "ProgressLearning focusReflect",
            "748": "ProgressValuingAct1",
            "754": "ProgressValuingAct2",
            "761": "ProgressValuingAct3",
            "768": "ProgressValuingPrepare",
            "804": "ProgressPersistenceAct3",
            "780": "ProgressValuingReflect",
            "790": "ProgressPersistenceAct1",
            "795": "ProgressPersistenceAct2",
            "814": "ProgressPersistencePrepare",
            "826": "ProgressPersistenceReflect",
            "836": "ProgressPlanningAct1",
            "851": "ProgressPlanningAct2",
            "865": "ProgressPlanningAct3",
            "878": "ProgressPlanningPrepare",
            "890": "ProgressPlanningReflect",
            "900": "ProgressTask managementAct1",
            "921": "ProgressTask managementAct2",
            "927": "ProgressTask managementAct3",
            "932": "ProgressTask managementPrepare",
            "944": "ProgressTask managementReflect"
        }

        requests = EventLog.query.filter(EventLog.timestamp.between(start_time, end_time)).\
            order_by(asc(EventLog.timestamp)).all()
        constructs = Construct.query.all()
        name_for_construct_id = {}
        for construct in constructs:
            name_for_construct_id[construct.id] = construct.name

        output = io.StringIO()
        writer = csv.writer(output)
        header = [
            'count', 'StudentId', 'SessionNo', 'SubSession', 'TimestampLogin', 'TimestampLastInteraction',
            'TimestampStartQuestionnaire', 'TimestampSubmitQuestionnaire', 'LanguageStartQuestionnaire',
            'LanguageSubmitQuestionnaire', 'FinishedQuestionnaire', 'TutorialVideoWatched(Popup)',
            'TutorialVideoWatched(Before1stQuest.Submission)', 'Gender', 'Studyprogram',
            'Academicyear'
        ]
        for count in range(1, 45):
            header.append(f"MESQuestion{count}")
        for count in range(1, 11):
            header.append(f"GSQQuestion{count}")

        header.extend([
            "Negative Motivation",
            "Anxiety",
            "Failure avoidance",
            "Uncertain control",
            "Negative Engagement",
            "Self-sabotage",
            "Disengagement",
            "Positive Motivation",
            "Self belief",
            "Learning focus",
            "Valuing",
            "Positive Engagement",
            "Persistence",
            "Planning",
            "Task management",
            "Interpersonal group work skills",
            "Task group work skills"
        ])

        for construct_name in name_for_construct_id.values():
            header.extend([
                f"Hover{construct_name}InGraphFrequency",
                f"Click{construct_name}InGraph",
                f"Hover{construct_name}InFeedbackCardFrequency",
                f"Hover{construct_name}InFeedbackCardTotalTime",
                f"Click{construct_name}Prepare",
                f"Progress{construct_name}Prepare",
                f"Click{construct_name}Act1",
                f"Progress{construct_name}Act1",
                f"Click{construct_name}Act2",
                f"Progress{construct_name}Act2",
                f"Click{construct_name}Act3",
                f"Progress{construct_name}Act3",
                f"Click{construct_name}Reflect",
                f"Progress{construct_name}Reflect",
                f"Click{construct_name}AdditionalSupport"
            ])

        writer.writerow(header)

        results = {}

        for request in requests:
            user_id = request.user_id
            session_id = request.session_id
            subsession = request.subsession
            if request.user_id not in results:
                results[user_id] = {}
            if request.session_id not in results[user_id]:
                results[user_id][session_id] = {}
            if request.subsession not in results[user_id][session_id]:
                results[user_id][session_id][subsession] = {
                    "user_id": request.user_id,
                    "session_id": request.session_id,
                    "subsession": request.subsession,
                    "count": 0,
                    "TimestampLogin": request.timestamp,
                    "TimestampLastInteraction": request.timestamp,
                    "TimestampStartQuestionnaire": None,
                    "TimestampSubmitQuestionnaire": None,
                    "LanguageStartQuestionnaire": None,
                    "LanguageSubmitQuestionnaire": None,
                    "FinishedQuestionnaire": 99,
                    "_videoWasPopup": None,
                    "TutorialVideoWatched(Popup)": None,
                    "TutorialVideoWatched(Before1stQuest.Submission)": None,
                    "Gender": None,
                    "Studyprogram": None,
                    "Academicyear": None,
                    "Negative Motivation": None,
                    "Anxiety": None,
                    "Failure avoidance": None,
                    "Uncertain control": None,
                    "Negative Engagement": None,
                    "Self-sabotage": None,
                    "Disengagement": None,
                    "Positive Motivation": None,
                    "Self belief": None,
                    "Learning focus": None,
                    "Valuing": None,
                    "Positive Engagement": None,
                    "Persistence": None,
                    "Planning": None,
                    "Task management": None,
                    "Interpersonal group work skills": None,
                    "Task group work skills": None,
                    "_selectedConstruct": None
                }
                for count in range(1, 45):
                    results[user_id][session_id][subsession][f"MESQuestion{count}"] = None
                for count in range(1, 11):
                    results[user_id][session_id][subsession][f"GSQQuestion{count}"] = None
                for construct_name in name_for_construct_id.values():
                    results[user_id][session_id][subsession][f"Hover{construct_name}InGraphFrequency"] = 0
                    results[user_id][session_id][subsession][f"Click{construct_name}InGraph"] = 0
                    results[user_id][session_id][subsession][f"Hover{construct_name}InFeedbackCardFrequency"] = 0
                    results[user_id][session_id][subsession][f"Hover{construct_name}InFeedbackCardTotalTime"] = 0
                    results[user_id][session_id][subsession][f"Click{construct_name}Prepare"] = 0
                    results[user_id][session_id][subsession][f"Progress{construct_name}Prepare"] = 99
                    results[user_id][session_id][subsession][f"Click{construct_name}Act1"] = 0
                    results[user_id][session_id][subsession][f"Progress{construct_name}Act1"] = 99
                    results[user_id][session_id][subsession][f"Click{construct_name}Act2"] = 0
                    results[user_id][session_id][subsession][f"Progress{construct_name}Act2"] = 99
                    results[user_id][session_id][subsession][f"Click{construct_name}Act3"] = 0
                    results[user_id][session_id][subsession][f"Progress{construct_name}Act3"] = 99
                    results[user_id][session_id][subsession][f"Click{construct_name}Reflect"] = 0
                    results[user_id][session_id][subsession][f"Progress{construct_name}Reflect"] = 99
                    results[user_id][session_id][subsession][f"Click{construct_name}AdditionalSupport"] = 0

            result = results[user_id][session_id][subsession]
            details = json.loads(request.details)

            result["count"] += 1
            if request.timestamp < result["TimestampLogin"]:
                result["TimestampLogin"] = request.timestamp
            if request.timestamp > result["TimestampLastInteraction"]:
                result["TimestampLastInteraction"] = request.timestamp
            if request.subject.name == "IntroductionVideoModal" and request.e_type.name == "Open":
                if "autoOpen" in details:
                    result["_timestampPopup"] = details["autoOpen"]
            if request.subject.name == "IntroductionVideoModal" and request.e_type.name == "Close":
                if result["_videoWasPopup"]:
                    result["TutorialVideoWatched(Popup)"] = details["timeWasOpen"] / 1000  # in seconds
                else:
                    # in seconds
                    result["TutorialVideoWatched(Before1stQuest.Submission)"] = details["timeWasOpen"] / 1000
            if request.subject.name == "PolarChart" and request.e_type.name == "Click":
                if "label" in details:
                    result[f"Click{details['label']}InGraph"] += 1
                    result['_selectedConstruct'] = details['label']
            if request.subject.name == "PolarChart" and request.e_type.name == "Hover":
                if "label" in details:
                    result[f"Hover{details['label']}InGraphFrequency"] += 1
            if request.subject.name == "FeedbackCard" and request.e_type.name == "Hover":
                if "length" in details and result["_selectedConstruct"] is not None:
                    result[f"Hover{result['_selectedConstruct']}InFeedbackCardFrequency"] += (details["length"] / 1000)
                    result[f"Hover{result['_selectedConstruct']}InFeedbackCardTotalTime"] += 1
            if request.subject.name == "PrepareModal" and request.e_type.name == "Open":
                if result["_selectedConstruct"] is not None:
                    result[f"Click{result['_selectedConstruct']}Prepare"] += 1
            if request.subject.name == "ReflectModal" and request.e_type.name == "Open":
                if result["_selectedConstruct"] is not None:
                    result[f"Click{result['_selectedConstruct']}Reflect"] += 1
            if request.subject.name == "LinkModal" and request.e_type.name == "Open":
                if result["_selectedConstruct"] is not None:
                    result[f"Click{result['_selectedConstruct']}AdditionalSupport"] += 1

        root = Collection.get_root_collection(required=True)
        user_id_for_actor = {}
        persons = md.Person.query.filter(md.Person.user_id.in_(root.all_user_ids)).all()
        for user in root.all_users:
            user_id_for_actor[str(user.actor)] = user.id
        for person in persons:
            user_id_for_actor[str(person.lrs_actor)] = person.user_id

        lrs_connector = root.main_lrs_connector()
        params = {
            # "statement.object.id": {"$in": )}
        }
        for statement in lrs_connector.model.get_statements(params):
            result = None
            if "result" not in statement:
                continue

            object_id = statement["object"]["id"]
            verb_id = statement["verb"]["id"]
            actor = str(statement["actor"].get("account", None))
            timestamp = strptime_frontend(statement["timestamp"])
            user_id = user_id_for_actor.get(actor, -1)
            if user_id not in results:
                continue
            for session_id in results[user_id].keys():
                for subsession in results[user_id][session_id].keys():
                    if timestamp > results[user_id][session_id][subsession]["TimestampLogin"] and \
                            timestamp < results[user_id][session_id][subsession]["TimestampLastInteraction"]:
                        result = results[user_id][session_id][subsession]
                        break
            if result is None:
                continue

            # Questionaire
            if verb_id == "http://adlnet.gov/expapi/verbs/initialized" and object_id.endswith("325"):
                result["TimestampStartQuestionnaire"] = timestamp
                if "context" in statement and statement["context"]["language"] is not None:
                    result["LanguageStartQuestionnaire"] = statement["context"]["language"]
            if verb_id == "http://adlnet.gov/expapi/verbs/completed" and object_id.endswith("325"):
                result["TimestampSubmitQuestionnaire"] = timestamp
                if "context" in statement and statement["context"]["language"] is not None:
                    result["LanguageSubmitQuestionnaire"] = statement["context"]["language"]

            if verb_id == "http://adlnet.gov/expapi/verbs/initialized" and object_id[-3:] in _activityHeaders.keys():
                if result[_activityHeaders[object_id[-3:]]] == 99:
                    result[_activityHeaders[object_id[-3:]]] = 0
            if verb_id == "http://adlnet.gov/expapi/verbs/completed" and object_id[-3:] in _activityHeaders.keys():
                result[_activityHeaders[object_id[-3:]]] = 1

            if verb_id == "http://adlnet.gov/expapi/verbs/answered":
                if object_id.endswith("960"):
                    result["Gender"] = statement["result"]["response"]
                if object_id.endswith("961"):
                    result["Studyprogram"] = statement["result"]["response"]
                if object_id.endswith("962"):
                    result["Academicyear"] = statement["result"]["response"]
                if int(object_id[-3:]) > 325 and int(object_id[-3:]) <= 369:
                    result[f"MESQuestion{int(object_id[-3:]) - 325}"] = statement["result"]["response"]
                if int(object_id[-3:]) > 369 and int(object_id[-3:]) <= 379:
                    result[f"GSQQuestion{int(object_id[-3:]) - 369}"] = statement["result"]["response"]

        user_scores = ScoresModel.get_construct_scores(
            collection_id=root.id,
            collection_ids=[],
            user_ids="all",
            activity_ids=None,
            construct_ids="all",
            start_time=start_time,
            end_time=end_time)

        for user_score in user_scores:
            if user_score["user_id"] not in results:
                continue
            # if user_score.max_score == 0:
            #     continue

            user_id = user_score["user_id"]
            timestamp = user_score["timestamp"]
            for session_id in results[user_id].keys():
                for subsession in results[user_id][session_id].keys():
                    if timestamp > results[user_id][session_id][subsession]["TimestampLogin"] and \
                            timestamp < results[user_id][session_id][subsession]["TimestampLastInteraction"]:
                        result = results[user_id][session_id][subsession]
                        break

            if result is None:
                continue

            result[name_for_construct_id[user_score["construct_id"]]] = user_score["score"]
            # float(user_score.score) / user_score.max_score * 100

        for user_id in results.keys():
            for session_id in results[user_id].keys():
                for subsession in results[user_id][session_id].keys():
                    result = results[user_id][session_id][subsession]

                    row = [
                        str(result["count"]),
                        str(result["user_id"]),
                        str(result["session_id"]),
                        str(result["subsession"]),
                        str(result["TimestampLogin"]),
                        str(result["TimestampLastInteraction"]),
                        str(result["TimestampStartQuestionnaire"]),
                        str(result["TimestampSubmitQuestionnaire"]),
                        str(result["LanguageStartQuestionnaire"]),
                        str(result["LanguageSubmitQuestionnaire"]),
                        str(result["FinishedQuestionnaire"]),
                        str(result["TutorialVideoWatched(Popup)"]),
                        str(result["TutorialVideoWatched(Before1stQuest.Submission)"]),
                        str(result["Gender"]),
                        str(result["Studyprogram"]),
                        str(result["Academicyear"])
                    ]
                    for count in range(1, 45):
                        row.append(str(result[f"MESQuestion{count}"]))
                    for count in range(1, 11):
                        row.append(str(result[f"GSQQuestion{count}"]))
                    row.extend([
                        str(result["Negative Motivation"]),
                        str(result["Anxiety"]),
                        str(result["Failure avoidance"]),
                        str(result["Uncertain control"]),
                        str(result["Negative Engagement"]),
                        str(result["Self-sabotage"]),
                        str(result["Disengagement"]),
                        str(result["Positive Motivation"]),
                        str(result["Self belief"]),
                        str(result["Learning focus"]),
                        str(result["Valuing"]),
                        str(result["Positive Engagement"]),
                        str(result["Persistence"]),
                        str(result["Planning"]),
                        str(result["Task management"]),
                        str(result["Interpersonal group work skills"]),
                        str(result["Task group work skills"])
                    ])

                    for construct_name in name_for_construct_id.values():
                        row.extend([
                            str(result[f"Hover{construct_name}InGraphFrequency"]),
                            str(result[f"Click{construct_name}InGraph"]),
                            str(result[f"Hover{construct_name}InFeedbackCardFrequency"]),
                            str(result[f"Hover{construct_name}InFeedbackCardTotalTime"]),
                            str(result[f"Click{construct_name}Prepare"]),
                            str(result[f"Progress{construct_name}Prepare"]),
                            str(result[f"Click{construct_name}Act1"]),
                            str(result[f"Progress{construct_name}Act1"]),
                            str(result[f"Click{construct_name}Act2"]),
                            str(result[f"Progress{construct_name}Act2"]),
                            str(result[f"Click{construct_name}Act3"]),
                            str(result[f"Progress{construct_name}Act3"]),
                            str(result[f"Click{construct_name}Reflect"]),
                            str(result[f"Progress{construct_name}Reflect"]),
                            str(result[f"Click{construct_name}AdditionalSupport"])
                        ])

                    writer.writerow(row)

        output.seek(0)
        return output

    @staticmethod
    def thermos_survey_report(start_time, end_time):
        _activityHeaders = {
            "325": "FinishedQuestionnaire"
        }
        requests = EventLog.query.filter(EventLog.timestamp.between(start_time, end_time)).\
            order_by(asc(EventLog.timestamp)).all()
        constructs = Construct.query.all()
        name_for_construct_id = {}
        for construct in constructs:
            name_for_construct_id[construct.id] = construct.name

        output = io.StringIO()
        writer = csv.writer(output)
        header = [
            'count', 'StudentId', 'TimestampSubmitQuestionnaire', 'LanguageStartQuestionnaire',
            'LanguageSubmitQuestionnaire', 'FinishedQuestionnaire', 'TutorialVideoWatched(Popup)',
            'TutorialVideoWatched(Before1stQuest.Submission)', 'Gender', 'Studyprogram',
            'Academicyear'
        ]
        for count in range(1, 45):
            header.append(f"MESQuestion{count}")
        for count in range(1, 11):
            header.append(f"GSQQuestion{count}")

        header.extend([
            "Negative Motivation",
            "Anxiety",
            "Failure avoidance",
            "Uncertain control",
            "Negative Engagement",
            "Self-sabotage",
            "Disengagement",
            "Positive Motivation",
            "Self belief",
            "Learning focus",
            "Valuing",
            "Positive Engagement",
            "Persistence",
            "Planning",
            "Task management",
            "Interpersonal group work skills",
            "Task group work skills"
        ])

        for count in range(1, 5):
            header.append(f"FeedbackQ{count}")

        writer.writerow(header)

        results = {}

        for request in requests:
            user_id = request.user_id
            session_id = request.session_id
            subsession = request.subsession
            if request.user_id not in results:
                results[user_id] = {
                    "user_id": request.user_id,
                    "count": 0,
                    "LanguageStartQuestionnaire": None,
                    "LanguageSubmitQuestionnaire": None,
                    "TimestampSubmitQuestionnaire": None,
                    "FinishedQuestionnaire": 99,
                    "_videoWasPopup": None,
                    "TutorialVideoWatched(Popup)": None,
                    "TutorialVideoWatched(Before1stQuest.Submission)": None,
                    "Gender": None,
                    "Studyprogram": None,
                    "Academicyear": None,
                    "Negative Motivation": None,
                    "Anxiety": None,
                    "Failure avoidance": None,
                    "Uncertain control": None,
                    "Negative Engagement": None,
                    "Self-sabotage": None,
                    "Disengagement": None,
                    "Positive Motivation": None,
                    "Self belief": None,
                    "Learning focus": None,
                    "Valuing": None,
                    "Positive Engagement": None,
                    "Persistence": None,
                    "Planning": None,
                    "Task management": None,
                    "Interpersonal group work skills": None,
                    "Task group work skills": None,
                    "_selectedConstruct": None
                }
                for count in range(1, 45):
                    results[user_id][f"MESQuestion{count}"] = None
                for count in range(1, 11):
                    results[user_id][f"GSQQuestion{count}"] = None
                for count in range(1, 5):
                    results[user_id][f"FeedbackQ{count}"] = None

            result = results[user_id]
            details = json.loads(request.details)

            result["count"] += 1
            if request.subject.name == "IntroductionVideoModal" and request.e_type.name == "Open":
                if "autoOpen" in details:
                    result["_timestampPopup"] = details["autoOpen"]
            if request.subject.name == "IntroductionVideoModal" and request.e_type.name == "Close":
                if result["_videoWasPopup"]:
                    result["TutorialVideoWatched(Popup)"] = details["timeWasOpen"] / 1000  # in seconds
                else:
                    # in seconds
                    result["TutorialVideoWatched(Before1stQuest.Submission)"] = details["timeWasOpen"] / 1000

        root = Collection.get_root_collection(required=True)
        user_id_for_actor = {}
        persons = md.Person.query.filter(md.Person.user_id.in_(root.all_user_ids)).all()
        for user in root.all_users:
            user_id_for_actor[str(user.actor)] = user.id
        for person in persons:
            user_id_for_actor[str(person.lrs_actor)] = person.user_id

        lrs_connector = root.main_lrs_connector()
        params = {
            # "statement.object.id": {"$in": )}
        }
        for statement in lrs_connector.model.get_statements(params):
            result = None
            if "result" not in statement:
                continue

            object_id = int(statement["object"]["id"].split('/')[-1])
            verb_id = statement["verb"]["id"]
            actor = str(statement["actor"].get("account", None))
            timestamp = strptime_frontend(statement["timestamp"])
            user_id = user_id_for_actor.get(actor, -1)
            if user_id not in results:
                continue
            result = results[user_id]
            if result is None:
                continue

            # Questionaire
            if verb_id == "http://adlnet.gov/expapi/verbs/initialized" and object_id == 325:
                if "context" in statement and statement["context"]["language"] is not None:
                    result["LanguageStartQuestionnaire"] = statement["context"]["language"]
            if verb_id == "http://adlnet.gov/expapi/verbs/completed" and object_id == 325:
                result["TimestampSubmitQuestionnaire"] = timestamp
                if "context" in statement and statement["context"]["language"] is not None:
                    result["LanguageSubmitQuestionnaire"] = statement["context"]["language"]

            if verb_id == "http://adlnet.gov/expapi/verbs/initialized" and object_id == 325:
                if result["FinishedQuestionnaire"] == 99:
                    result["FinishedQuestionnaire"] = 0
            if verb_id == "http://adlnet.gov/expapi/verbs/completed" and object_id == 325:
                result["FinishedQuestionnaire"] = 1

            if verb_id == "http://adlnet.gov/expapi/verbs/answered":
                if object_id == 960:
                    result["Gender"] = statement["result"]["response"]
                if object_id == 961:
                    result["Studyprogram"] = statement["result"]["response"]
                if object_id == 962:
                    result["Academicyear"] = statement["result"]["response"]
                if object_id > 325 and object_id <= 369:
                    result[f"MESQuestion{object_id - 325}"] = statement["result"]["response"]
                if object_id > 369 and object_id <= 379:
                    result[f"GSQQuestion{object_id - 369}"] = statement["result"]["response"]
                if object_id > 385 and object_id <= 389:
                    result[f"FeedbackQ{object_id - 385}"] = statement["result"]["response"]

        user_scores = ScoresModel.get_construct_scores(
            collection_id=root.id,
            collection_ids=[],
            user_ids="all",
            activity_ids=None,
            construct_ids="all",
            start_time=start_time,
            end_time=end_time)

        for user_score in user_scores:
            if user_score["user_id"] not in results:
                continue
            # if user_score.max_score == 0:
            #     continue

            user_id = user_score["user_id"]
            timestamp = user_score["timestamp"]
            result = results[user_id]

            if result is None:
                continue

            result[name_for_construct_id[user_score["construct_id"]]] = user_score["score"]
            # float(user_score.score) / user_score.max_score * 100

        for user_id in results.keys():
            result = results[user_id]

            row = [
                str(result["count"]),
                str(result["user_id"]),
                str(result["TimestampSubmitQuestionnaire"]),
                str(result["LanguageStartQuestionnaire"]),
                str(result["LanguageSubmitQuestionnaire"]),
                str(result["FinishedQuestionnaire"]),
                str(result["TutorialVideoWatched(Popup)"]),
                str(result["TutorialVideoWatched(Before1stQuest.Submission)"]),
                str(result["Gender"]),
                str(result["Studyprogram"]),
                str(result["Academicyear"])
            ]
            for count in range(1, 45):
                row.append(str(result[f"MESQuestion{count}"]))
            for count in range(1, 11):
                row.append(str(result[f"GSQQuestion{count}"]))
            row.extend([
                str(result["Negative Motivation"]),
                str(result["Anxiety"]),
                str(result["Failure avoidance"]),
                str(result["Uncertain control"]),
                str(result["Negative Engagement"]),
                str(result["Self-sabotage"]),
                str(result["Disengagement"]),
                str(result["Positive Motivation"]),
                str(result["Self belief"]),
                str(result["Learning focus"]),
                str(result["Valuing"]),
                str(result["Positive Engagement"]),
                str(result["Persistence"]),
                str(result["Planning"]),
                str(result["Task management"]),
                str(result["Interpersonal group work skills"]),
                str(result["Task group work skills"])
            ])
            for count in range(1, 5):
                row.append(str(result[f"FeedbackQ{count}"]))

            writer.writerow(row)

        output.seek(0)
        return output
