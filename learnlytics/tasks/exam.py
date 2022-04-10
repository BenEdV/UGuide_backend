import learnlytics.database.studydata as md
from learnlytics.extensions import celery


@celery.task
def load_results(exam_id):
    print(f"Loading results of exam with id {exam_id}")
    exam = md.Activity.get(exam_id)
    if exam is None:
        print(f"Exam could not be found")
        return
    md.Activity.load_result(exam.id)
