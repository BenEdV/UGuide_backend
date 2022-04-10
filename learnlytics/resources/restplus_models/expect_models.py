"""
The recourses for the models for the expected values of the API fields
"""

from flask_restplus import fields

from create_api import usersns, coursesns, currentuserns, authorizationns, loggingns, modelns

# Person Namespace Models

student_fields = usersns.model("Students", {
    "students": fields.List(fields.String,
                            example=["student1", "student2"])
})

# Courses Namespace Models

post_course_exam_user_fields = coursesns.model("Test", {"students": fields.List(fields.String,
                                                                                example=["local_biol_7"])})

# TODO: Create proper questions
put_course_exam_user_fields = coursesns.model("Test", {"title": fields.String(example="Testexamen"),
                                                       "type": fields.String(example="Multiple Choice"),
                                                       "max_score": fields.Integer(example=50),
                                                       "course_id": fields.String(example="B-B1MB05"),
                                                       "questions": fields.List(fields.String(example=["Test"]))})

# Currentuser Namespace Models

auth_fields = currentuserns.model('AuthResource', {'username': fields.String(required=True, example="0000005"),
                                                   'password': fields.String(required=True, example="test")})

reg_fields = currentuserns.model('RegisterResource', {'username': fields.String(required=True, example="0000005"),
                                                      'password': fields.String(required=True, example="test"),
                                                      'captcha_token': fields.String(required=True)})


setting_fields = currentuserns.model("setting_data", {
    "exams": fields.List(fields.Integer, example=[2, 3]),
    "group": fields.String(example="cohort"),
    "misconcepts": fields.Boolean(example=False)
})

post_user_settings_fields = currentuserns.model("CourseUserSettings", {
    'language': fields.String(example="en"),
    'B-B1MB05': fields.Nested(setting_fields)
})

# Authorization Namespace Models

post_fields = authorizationns.model("Collection", {
    "name": fields.String(example="student", description="Name of the role"),
    "id": fields.String(required=True, example="B-B1BEP13", description="Id of the collection"),
    "parent_id": fields.String(example="UU", description="Id of the parent collection")})

authorization_collection_post_fields = authorizationns.model("Roles", {
    "name": fields.String(example="testrole", description="Name of the role"),
    "col_id": fields.String(required=True, example="Informatica", description="Id of the collection"),
    "permissions": fields.List(fields.String, example=["read_own_data", "read_aggregated_data"],
                               description="Lijst van de toe te voegen concepten")})

authorization_user_permission_post_fields = authorizationns.model("UserRoles", {
    "remove": fields.Boolean(example="False"),
    "users": fields.List(fields.String, example=["arian_loc", "patrick_loc"], description="List of person ids")})


authorization_roles_post_fields = authorizationns.model("UserDataRoles", {
    "permissions": fields.List(fields.String, example=["read_own_data", "read_aggregated_data"],
                               description="List of person ids")})

# Logging Namespace Models
post_logging_state_fields = loggingns.model("LoggingState", {
    'from_state': fields.String(required=True, example="teacherContainer.courseDashboard"),
    'to_state': fields.String(required=True, example="teacherContainer.courseDashboard.exams"),
    'timestamp': fields.String(required=True, example="2018-09-25 12:30:01")
})

post_logging_event_fields = loggingns.model("LoggingEvent", {
    'current_state': fields.String(required=True, example="teacherContainer.courseDashboard"),
    'details': fields.String(required=True, example="Test"),
    'timestamp': fields.String(required=True, example="2018-09-25 12:30:01")
})

post_report_fields = loggingns.model("LoggingReport", {
    'start_time': fields.String(required=True, example="2018-09-25 12:30:01"),
    'end_time': fields.String(required=True, example="2018-09-25 12:30:01"),
    'path': fields.String(required=True, example="/currentuser/authentication")
})

# Model and Construct Namespace Model

post_model_fields = modelns.model("PostModel", {
    "name": fields.String(example="Model name"),
    "description": fields.String(example="Description"),
    "weight": fields.Integer(example=1)
})

post_construct_fields = modelns.model("PostConstruct", {
    "name": fields.String(example="Construct name"),
    "model_id": fields.Integer(example=1),
    "description": fields.String(example="Description"),
    "weight": fields.Integer(example=1),
    "parent_id": fields.Integer(example=-1),
})
