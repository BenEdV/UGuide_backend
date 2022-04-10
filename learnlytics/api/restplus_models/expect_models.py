from flask_restplus import fields

from create_api import api_exams_ns, api_auth_ns, api_authorization_ns, api_people_ns, api_courses_ns

# post authentication

post_auth_fields = api_auth_ns.model("Authentication", {
    "api_key": fields.String(example="6ee41982-048d-4a92-8d83-ccdc08a9002b"),
})

# post register api_key

post_register_key_fields = api_authorization_ns.model("Authorization", {
    "requester": fields.String(example="admin_genoom"),
    "course_code": fields.String(example="B-B1EXST13")
})

# post exam

post_exam_answer = api_exams_ns.model("Answer", {
    "answer_id": fields.String(example="1"),
    "body": fields.String(example="Madrid"),
    "correct": fields.Boolean(example=True),
    "score": fields.Float(example=10.0)
})

post_exam_question = api_exams_ns.model("Question", {
    "question_id": fields.String(example="b73ea970-c1e1-8d45-d9cd-fd75f2eb6545"),
    "type": fields.String(example="Multiple Choice"),
    "body": fields.String(example="What is the capital of Spain?"),
    "max_score": fields.Integer(example=5),
    "p_value": fields.Float(example=0.42708333333333),
    "std_value": fields.Float(example=0.49465458627432),
    "rit_value": fields.Float(example=0.44230280638001),
    "rir_value": fields.Float(example=0.22221066908645),
    "answers": fields.List(fields.Nested(post_exam_answer)),
})

post_exam_fields = api_exams_ns.model("Exam", {
    "remote_exam_id": fields.String(required=True, example="58621"),
    "title": fields.String(example="Deeltentamen 1"),
    "type": fields.String(example="exam"),
    "date": fields.String(example="2017-04-11"),
    "max-score": fields.Float(example=10.0),
    "questions": fields.List(fields.Nested(post_exam_question))
})

post_exams_fields = api_exams_ns.model("Exams", {
    "exams": fields.List(fields.Nested(post_exam_fields)),
})

# post exam results

post_question_result = api_exams_ns.model("QuestionResult", {
    "result_id": fields.String(required=True, example="00000000001"),
    "question_id": fields.String(example="b73ea970-c1e1-8d45-d9cd-fd75f2eb6545"),
    "given_answer": fields.String(example="A"),
    "given_answer_id": fields.String(example="001"),
    "score": fields.Float(example=1.0),
})

post_exam_result_fields = api_exams_ns.model("Result", {
    "results_id": fields.String(required=True, example="00000000001"),
    "user_id": fields.String(required=True, example="uu_test_student"),
    "exam_id": fields.String(required=True, example="58621"),
    "grade": fields.Float(example=7.9),
    "score": fields.Float(example=42.1),
    "question_results": fields.List(fields.Nested(post_question_result))
})

post_exam_results_fields = api_exams_ns.model("Results", {
    "exam_results": fields.List(fields.Nested(post_exam_result_fields)),
})

# post course

post_course_fields = api_courses_ns.model("Course", {
    "id": fields.String(required=True, example="1"),
    "name": fields.String(example="Introduction to Biology")
})

post_courses_fields = api_courses_ns.model("Courses", {
    "courses": fields.List(fields.Nested(post_course_fields))
})
