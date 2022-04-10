
from flask_restplus import Api
from flask import Blueprint

# This files allows the import of the api, so that we can add the routes in various other files

# LearnLytics API

learnlytics_blueprint = Blueprint('learnlytics', __name__)
api = Api(learnlytics_blueprint,
          doc='/doc',
          version='1.0',
          title='Learnlytics Resources API',
          description='The LearnLytics frontend dataprovider')

# LearnLytics Namespaces

authenticationns = api.namespace(
    'Authentication',
    path="/authentication",
    description="Operations related to the authentication (logging in, registering, changing password")
api.add_namespace(authenticationns)

authorizationns = api.namespace('Authorization',
                                path="/authorization",
                                description="Operations related to the authorization tree")
api.add_namespace(authorizationns)

coursesns = api.namespace('Courses',
                          path='/course',
                          description="Operations on all courses")
api.add_namespace(coursesns)

course_instances_ns = api.namespace(
    'Course Instances',
    path='/course_ins',
    description="Operations on all course instances")
api.add_namespace(course_instances_ns)

periods_ns = api.namespace(
    'Periods',
    path='/periods',
    description="Operations on all periods")
api.add_namespace(periods_ns)

currentuserns = api.namespace('Current user',
                              path="/currentuser",
                              description="Operations for the current user")
api.add_namespace(currentuserns)

loggingns = api.namespace('Logging',
                          path="/logging",
                          description="Operations for reqlogging activities of the current user")
api.add_namespace(loggingns)

activity_ns = api.namespace(
    "Activity",
    path="/<int:collection_id>/activities",
    description="Operations for activities of a specific collection")
api.add_namespace(activity_ns)

score_ns = api.namespace(
    "Score",
    path="/<int:collection_id>/scores",
    description="Operations for scores of a specific collection")
api.add_namespace(activity_ns)

usersns = api.namespace(
    'Users',
    path="/<int:collection_id>/users",
    description="Operations on users of a specific collection")
api.add_namespace(usersns)

groupsns = api.namespace(
    'Groups',
    path="/<int:collection_id>/groups",
    description="Operations on groups of a specific collection")
api.add_namespace(groupsns)

external_ns = api.namespace(
    'External',
    path="/external",
    description="Operations related to loading data from external resources")
api.add_namespace(external_ns)

modelns = api.namespace(
    'Model',
    path="/<int:collection_id>/models",
    description="Operations related to models and constructs")
api.add_namespace(modelns)

connector_ns = api.namespace(
    'Connector',
    path="/<int:collection_id>/connector",
    description="Operations related to loading data from connectors for a collection")
api.add_namespace(external_ns)

utilns = api.namespace(
    'Utility',
    path="/util",
    description="Operations related to test calls not used by the frontend")
api.add_namespace(utilns)

home_ns = api.namespace(
    'Home',
    path="/home",
    description="Operations related to loading data relevant for the home page")
api.add_namespace(home_ns)

type_ns = api.namespace(
    'Type',
    path="/<int:collection_id>/type",
    description="Information about the types supported by the backend")
api.add_namespace(type_ns)

xapi_ns = api.namespace(
    'XAPI',
    path="/xapi",
    description="XAPI endpoint")
api.add_namespace(xapi_ns)

# Connector API

connector_blueprint = Blueprint('connector', __name__, url_prefix='/connector')
connector_api = Api(connector_blueprint,
                    doc='/doc',
                    version='0.1',
                    title='Learnlytics Connector API',
                    description='The LearnLytics integration provider')

# Connector Namespaces

remindons = connector_api.namespace('Remindo',
                                    path="/remindo",
                                    description="Remindo operations")
connector_api.add_namespace(remindons)

csvns = connector_api.namespace('CSV',
                                path="/csv",
                                description="CSV-file operations")
connector_api.add_namespace(csvns)

# General API

general_api_blueprint = Blueprint('General', __name__, url_prefix='/api')
general_api = Api(general_api_blueprint,
                  doc='/doc',
                  version='0.1',
                  title='Learnlytics API',
                  validate=True,
                  description='The LearnLytics API')


api_auth_ns = general_api.namespace('Authenticate',
                                    path="/auth",
                                    description="Operations to authenticate the API")
general_api.add_namespace(api_auth_ns)

api_exams_ns = general_api.namespace('Exams',
                                     path="/exams",
                                     description="Operations to add exams to LearnLytics")
general_api.add_namespace(api_exams_ns)

api_people_ns = general_api.namespace('People',
                                      path="/people",
                                      description="Operations to add people to LearnLytics")
general_api.add_namespace(api_people_ns)


api_authorization_ns = general_api.namespace('Authorization',
                                             path="/authorization",
                                             description="Operations to authorize the API")
general_api.add_namespace(api_authorization_ns)

api_users_ns = general_api.namespace('Users',
                                     path="/users",
                                     description="Operations to add users to LearnLytics")
general_api.add_namespace(api_users_ns)

api_courses_ns = general_api.namespace('Courses',
                                       path="/courses",
                                       description="Operations to add courses to LearnLytics")
general_api.add_namespace(api_courses_ns)

api_user_ns = general_api.namespace('User',
                                    path="/",
                                    description="Operations to add users to courses")
general_api.add_namespace(api_user_ns)

# Widgets

widget_blueprint = Blueprint('Widgets', __name__, url_prefix='/widget')
widget_api = Api(
    widget_blueprint,
    doc='/doc',
    version='0.1',
    title='Learnlytics Widget API',
    validate=True,
    description='The LearnLytics Widget API'
)

widget_hello_ns = widget_api.namespace(
    'Hello World',
    path="/hello",
    description="Hello World endpoint to test connectivity"
)
widget_api.add_namespace(widget_hello_ns)

widget_constructs_ns = widget_api.namespace(
    'Constructs',
    path="/<int:collection_id>/constructs",
    description="Widgets for constructs")
api.add_namespace(widget_constructs_ns)


# Constructs & Models

modelns = api.namespace(
    'Model',
    path="/<int:collection_id>/models",
    description="Operations related to models and constructs")
api.add_namespace(modelns)
