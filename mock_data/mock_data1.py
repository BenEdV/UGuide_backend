
# pylint: skip-file

"""
Contains the exam-data for the meta-database
"""

import random
import datetime
import sys

from learnlytics.analyse.question_value import update_p_value, update_std_value, update_rit_value, update_rir_value
from learnlytics.analyse.exam import update_exam_score, update_exam_max_score
from learnlytics.analyse.question import update_question_score, update_question_max_score
from learnlytics.api.models.authorization import add_api_key_permission
import learnlytics.authorization.manager as auth
from learnlytics.database.api.apikey import APIKey
import learnlytics.database.studydata as md
from learnlytics.database.authorization.user import User, UserPassHash
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.role import Role
from learnlytics.database.authorization import init_authorization_db
from learnlytics.database.api import add_gen_api_permissions

names = [
    "", "Ben", "Laura", "Minh-An", "Bram", "Sven", "Cas", "Gerco", "Paul", "Olivier", "Nelia", "Colin", "Evelin",
    "Miss", "Jena", "Genny", "Charlena", "Carmelo", "Willow", "Karmen", "Lillian", "Raymon", "Titus",
    "Hsiu", "Troy", "Eusebio", "Sharee", "Tiara", "Nolan", "Becki", "Walker", "Sharen", "Lucia", "Alda",
    "Christiana", "Vera", "Sparkle", "Katelynn", "Meaghan", "Francis", "Zella", "Holli", "Anastasia", "Elease",
    "Josiah", "Heather", "Candance", "Glynis", "Frida", "Loan", "Kindra", "Tammy", "Shayna", "Cheryl", "Eden",
    "Jessia", "Carlo", "Elana", "Joanie", "Glenda", "Jessi", "Elden", "Dolly", "Hayley", "Alejandra", "Kathyrn",
    "Tambra", "Alphonse", "Margie", "Marlana", "Caroyln", "Buena", "Sage", "Cheryll", "Tova", "Laila", "Freda",
    "Elouise", "Ramona", "Thomasena", "Loria", "Annetta", "Ernestine", "Broderick", "Jodi", "Eda", "Sylvester",
    "Angeline", "Vertie", "Beth", "Yadira", "Lea", "Fernando", "Gaylene", "Federico", "Virginia", "Haydee", "Kori",
    "Adan", "Verla", "Colin", "Serita", "Selena", "Tillie", "Kayleen", "Carolin", "Amina", "Ria", "Lucretia",
    "Priscilla", "Maudie", "Raquel", "Clarence", "Eddy", "Jenniffer", "Hattie", "Ione", "Evon", "Etha", "Anglea",
    "Delorse", "Andree", "Neomi", "Alaine", "Tiera", "Coralee", "Yuriko", "Elizabet", "Raina", "Enid", "Joy",
    "Billye", "Twila", "Ethelene", "Gala", "Julieta", "Arthur", "Lizeth", "Chiquita", "Manual", "Cristopher",
    "Stephani", "Shawana", "Lazaro", "Hillary", "Nga", "Leeanna", "Berna", "Kathleen", "Shanta", "Inger",
    "Bernardo", "Sharan", "Patrica", "Nicola", "Savannah", "Lanette", "Lucilla", "Otelia", "Lucie", "Leland",
    "Dionna", "Zita", "Shu", "Kattie", "Enid", "Hector", "Porsha", "Caryn", "Nigel", "China", "Helen", "Ethyl",
    "Loretta", "Mandi", "Jona", "Wilbert", "Moshe", "Deandre", "Dianne", "Irving", "Reta", "Yoshie", "Sonya",
    "Elina", "Solomon", "Cora", "Veronique", "Kacie", "Truman", "Micah", "Shameka", "Manda", "Jeffrey", "Nisha",
    "Deeann", "Bridget", "Glory", "Carlyn", "Aundrea", "Carlo", "Catharine", "Luisa", "Candy", "Alyson", "Debrah",
    "Misha", "Malinda", "Tamera", "Vern", "Al", "Clemente", "Tyson", "Blanca", "Zulma", "Dyan", "Tisa", "Caryl",
    "Ellis", "Mattie", "Mayola", "Annelle", "Audry", "Latoya", "Shaneka", "Jerrica", "Fred", "Carry", "Charles",
    "Cesar", "Jung", "Casie", "Loyce", "Glayds", "Gilberte", "Jammie", "Chelsey", "Bobbye", "Russ", "Heriberto",
    "Domenica", "Euna", "Irina", "Sherlene", "Daron", "Prince", "Fidelia", "Merrie", "Gaylord", "Yen", "Jolene",
    "Madelyn", "Elza", "Illa", "Zackary", "Jonas", "Argentina", "Fernande", "Mose", "Ayana", "Vickey", "Kali",
    "Angelia", "Haley", "Ione", "Francoise", "Raeann", "Bethann", "Joana", "Lena", "Zoraida", "Aisha", "Bettina",
    "Lenna", "Teri", "Kimberlee", "Audrea", "Hettie", "Jenna", "Daren", "Shenna", "Liana", "Jonna", "Lashay",
    "Dortha", "Keenan", "Nery", "Daria", "Staci", "Bud", "Elanor", "Ewa", "Loise", "Karin", "Danae", "Marielle",
    "Stephany", "Randell", "Rosy", "Quentin", "Kathyrn", "Berenice", "Lore", "Deidra", "Lorean", "Reda", "Mammie",
    "Graham", "Jorge", "Williams", "Spencer", "Darell", "Stefania", "Earlean", "Troy", "Detra", "Caitlyn",
    "Matthew", "Houston", "Natalie", "Ivy", "Cira", "Burl", "Annis", "Victor", "Shon", "Yer", "Franklin", "Isa",
    "Bobbie", "Margot", "Queen", "Kara", "Alona", "Romelia", "Marylyn", "Lamont", "Filiberto", "Frida", "Sima",
]

last_names = [
    "Allen", "Gallegos", "Simon", "French", "Cunningham", "Barton", "Johns", "Ware", "Vaughan", "Kelley",
    "Ayers", "Owen", "Douglas", "Obrien", "Page", "Barnes", "Chambers", "Moses", "Morris", "Adams", "Ryan", "Golden",
    "Tate", "Watts", "Holder", "Conway", "Anderson", "Ballard", "Hansen", "Ewing", "Dunn", "Thornton", "Horton",
    "Roberson", "Weber", "Whitney", "Farrell", "Simmons", "Kirk", "Baird", "Spence", "Kim", "Olson", "Hayes",
    "Faulkner", "Hensley", "Campbell", "Waller", "Cruz", "Arroyo", "Reyes", "Vazquez", "Acevedo", "Mann", "Sheppard",
    "Small", "Mckenzie", "Torres", "Daniels", "Ellis", "Baldwin", "Ramsey", "Hull", "Sweeney", "Atkins", "Lang",
    "Waller", "Mooney", "Harrison", "Reynolds", "Bush", "Shannon", "Martinez", "Maxwell", "Fleming", "Hernandez",
    "Levine", "Montoya", "Higgins", "Quinn", "Jimenez", "Mata", "Mccarthy", "Jefferson", "Sweeney", "Hoffman", "Hansen",
    "Benton", "Jacobson", "Daniel", "Reyes", "Schroeder", "Torres", "Little", "Cameron", "Bartlett", "Browning", "Meza",
    "Mayer", "Proctor", "Daines", "Vogt", "Cobuzzi", "Cottee", "Bouchard", "Odlyzko", "Gill", "Iuculano", "Joltes",
    "Sheehy", "Kangis", "Ferguson", "Benedetti", "Xia", "Kurosaka", "Metting", "Kollmann", "Tranmer", "Stilgoe", "York",
    "Scarsini", "Ottlinger", "Hardison", "Welsch", "Guay", "Tulikangas", "Staples", "Runyon", "Spacks", "Goodale",
    "Kalman", "Gravett", "Carney", "Fruhan", "Ricart-costa", "Slone", "Knapp", "Fritzsche", "Iyer", "Nathans",
    "Goodall", "Heller", "Wakeham", "Shin", "Dalaklis", "Kommer", "Grow", "Maine-hershey", "Bempechat", "Altenberger",
    "Wan", "Burgess", "Eskandari-qajar", "Cabot", "Siegrist", "Napolilli", "Farabella", "Sperazzo", "Nagle", "Landes",
    "Ott", "Lukibisi", "Ruchames", "Zimbel", "Weisert", "Dini", "Leoni", "Stedman", "Bisaga", "Faucher", "Danaher",
    "Kohl", "Mazza", "Robledo", "Sassetti", "De wilde", "Debold", "Dagum", "Nevins", "Sekoni", "Mullen", "Maas",
    "Marcos", "Siemiginowska", "Bading", "Paciatori", "Houck", "Tretter", "Bolstad", "Ru", "Mckay", "Resta",
    "Featherson", "Rodriguez", "Yong", "Allebach", "Maller", "Tribbett", "Mitten", "Correia", "Gozzi", "Finau",
    "Shanks", "Shirazi", "Ceniceros", "Bergstrom", "Gauthier", "Prokopow", "Gibor", "Blodgett", "Rasanen", "Lemon",
    "Conrad", "Colnago", "Ge", "Welsh-carroll", "Laidler", "Fowler", "Glebus", "Beal", "Cleary", "Mcpherson", "Gorton",
    "Marcum", "Rabino", "Kracov", "Jaimes-freyre", "Bastian", "Coakley", "Valencik", "Christiansen", "Bernheimer",
    "Hopper", "Harmeling", "Shan", "Fan", "Macpherson", "Guenther", "Parris", "Partridge", "Kharajian", "Takaesu",
    "Capra", "Heinrich", "Cecchini", "Estrada", "Tierney", "Ajimura", "Bills", "Vorperian", "Conlin", "Bonwitt",
    "Modestino", "Comolli", "Votey", "Arm", "Skinner", "Clews", "Stubson", "Shannon", "Engquist", "Frampton", "Runge",
    "Townsley", "Tan", "Federer", "Sinclair", "Clapp", "Parkman", "Koolaard", "Riegler", "Engelhart", "Biolos",
    "Grimsted", "Zahedi", "Sniffen", "Caspar", "Barone", "Kornbrot", "Melita", "Rizzi", "Strehlow", "Driesse",
    "Langosy", "Pieri", "Iaquinta", "Schellenberg", "De gunst", "Klumpar", "Degalarce", "Whitehead", "Lonoff", "Dames",
    "Fernandez", "Parenteau", "Spink", "Liddell", "Danielson", "Corazzini", "Gillette", "Boothe", "Mc ghee", "Chall",
    "Yalman", "Weissman", "Jucks", "Pappenheimer", "Belaoussof", "Fauth", "Arntz", "Trivellato", "Ackerman", "Pocock",
    "Leskow", "Tseko", "Papert", "Goodman", "Spillane", "Hutchcroft", "Shroff", "Fick", "Mcmullin", "Sebastiani",
    "Tananbaum", "Van doren", "Lauritsen", "Tronick", "Noremberg", "Rodman", "Topulos", "Nguyen", "Nennig", "Wingfield"]

course_names = [
    {"name": "Biologie en ecologie van planten", "code": "B-B1BEP13"},
    {"name": "Moleculaire biologie", "code": "B-B1MB05"},
    {"name": "Systeembiologie", "code": "B-B1SYSB09"},
    {"name": "Biologie van dieren", "code": "B-B1DIER05"},
    {"name": "Experiment en statistiek", "code": "B-B1EXST13"}
]


class MockDatabase(object):  # pylint: disable=too-few-public-methods, missing-docstring
    def __init__(self, db):
        """
        Initiate the mockdatabase with given database
        :param db: database
        """
        self.db = db
        # self.auth = get_auth_manager()
        self.faculties = list()
        self.courses = list()
        self.studies = list()
        self.root = list()
        self.admins = list()
        self.teachers = list()
        self.students = list()
        self.participation_rate = 100

    def single_course(self, num_students=40, num_groups=4):
        """
        Creates a single course with one teacher
        """
        self.root_indices = []
        self.admin_indices = range(1, 2)
        self.teacher_indices = range(2, 3)
        self.student_indices = range(3, 3 + num_students)
        self.all_indices = range(1, 3 + num_students)

        self.root_ids = []
        self.admin_ids = ["mock_" + str(i) for i in self.admin_indices]
        self.teacher_ids = ["mock_" + str(i) for i in self.teacher_indices]
        self.student_ids = ["mock_" + str(i) for i in self.student_indices]
        self.all_ids = self.root_ids + self.admin_ids + self.teacher_ids + self.student_ids
        self.password = "test"

        self.course_info = [{"name": "Biologie en ecologie van planten", "code": "B-B1BEP13"}]
        self.general_api_key = ""

        self.group_ids = range(1, num_groups + 1)

        self.add_users()
        self.add_collection_tree()
        self.add_courses()
        self.add_root_api_key()
        self.add_general_api_permissions()
        self.add_usergroups()
        self.link_users_to_courses()
        self.link_users_to_groups()
        self.add_concept_model()

        self.db.session.commit()

    def fill_data(self, num_students=40, num_groups=4, participation_rate=100, gen_results=True, gen_scores=True):
        """
        Fills the database with the data of the mock-exam
        """
        # pylint: disable=too-many-statements
        if not Role.get_name("student", required=False):
            print("No roles were found. First run ./create_metadb.py")
            sys.exit(1)

        self.root_indices = range(1, 2)
        self.admin_indices = range(2, 4)
        self.teacher_indices = range(4, 8)
        self.student_indices = range(8, 8 + num_students)
        self.all_indices = range(1, 8 + num_students)

        self.root_ids = ["mock_" + str(i) for i in self.root_indices]
        self.admin_ids = ["mock_" + str(i) for i in self.admin_indices]
        self.teacher_ids = ["mock_" + str(i) for i in self.teacher_indices]
        self.student_ids = ["mock_" + str(i) for i in self.student_indices]
        self.all_ids = self.root_ids + self.admin_ids + self.teacher_ids + self.student_ids
        self.password = "test"

        self.course_info = [
            {"name": "Biologie en ecologie van planten", "code": "B-B1BEP13"},
            {"name": "Moleculaire biologie", "code": "B-B1MB05"},
            {"name": "Systeembiologie", "code": "B-B1SYSB09"},
            {"name": "Biologie van dieren", "code": "B-B1DIER05"},
            {"name": "Experiment en statistiek", "code": "B-B1EXST13"}
        ]

        self.general_api_key = ""

        self.participation_rate = participation_rate

        self.group_ids = range(1, num_groups + 1)

        self.add_users()
        self.add_collection_tree()
        self.add_courses()
        self.add_root_api_key()
        self.add_general_api_permissions()
        self.add_usergroups()
        self.link_users_to_courses()
        self.link_users_to_groups()
        self.add_concept_model()

        if gen_results:
            import mock_data.mult_choice_bio as bio
            import mock_data.mult_choice_1 as mult1
            import mock_data.mult_choice_2 as mult2
            import mock_data.mult_choice_wisk as wisk

            self.add_mult_choice_exam("Bio Toets Oefening", md.Course.get_code("B-B1MB05"), mult1.examdata)
            self.add_mult_choice_exam("Bio Toets Tussentoets", md.Course.get_code("B-B1MB05"), bio.examdata)
            self.add_mult_choice_exam("Bio Toets Eindtoets", md.Course.get_code("B-B1MB05"), mult2.examdata)

            self.add_mult_choice_exam("Statistiek Oefening", md.Course.get_code("B-B1EXST13"), wisk.examdata)
            self.add_mult_choice_exam("Statistiek Eindtoets", md.Course.get_code("B-B1EXST13"), mult2.examdata)

        self.db.session.commit()
        # Removes the session

        # self.db.session.remove()

    def add_general_api_permissions(self):
        add_gen_api_permissions()
        add_api_key_permission(self.api_key.id, "add_person", 1)
        add_api_key_permission(self.api_key.id, "add_exam", self.courses[0].collection_id)
        add_api_key_permission(self.api_key.id, "add_exam_result", self.courses[0].collection_id)

    def add_root_api_key(self):
        self.api_key = APIKey.add_api_key(self.general_api_key, "root")

    def add_collection_tree(self):
        beta_collection = Collection.get_name("Betawetenschappen")
        if beta_collection:
            self.beta = beta_collection.id
        else:
            self.beta = auth.add_collection("Betawetenschappen", parent_id=1).id

        bio_collection = Collection.get_name("Biologie")
        if bio_collection:
            self.bio = bio_collection.id
        else:
            self.bio = auth.add_collection("Biologie", parent_id=self.beta).id

    def add_courses(self):
        end_date = datetime.date.today() + datetime.timedelta(days=80)

        for course in self.course_info:
            self.courses.append(
                md.Course(
                    name=course["name"],
                    collection_parent_id=self.bio,
                    code=course["code"],
                    start_date=datetime.date.today(),
                    end_date=end_date
                )
            )

        self.db.session.add_all(self.courses)
        self.db.session.flush()

    name_index = 0

    def add_mock_user(self, id):
        self.name_index += 1
        return User(
            id,
            "local",
            names[self.name_index] + " " + last_names[self.name_index],
            names[self.name_index] + "@test.com",
            names[self.name_index],
            last_names[self.name_index]
        )

    def add_users(self):
        """
        Add users with password test
        """
        for i in self.root_ids:
            self.root.append(self.add_mock_user(i))

        for i in self.admin_ids:
            self.admins.append(self.add_mock_user(i))

        for i in self.teacher_ids:
            self.teachers.append(self.add_mock_user(i))

        for i in self.student_ids:
            self.students.append(self.add_mock_user(i))

        self.db.session.add_all(self.root)
        self.db.session.add_all(self.admins)
        self.db.session.add_all(self.teachers)
        self.db.session.add_all(self.students)

        self.db.session.flush()

        for i in self.all_ids:
            self.db.session.add(UserPassHash("local_" + i, self.password))

        # Give Remindo permissions
        for teacher in self.teachers:
            remindo_collection = Collection.get_name("remindo")
            auth.add_user_role(teacher.key, "teacher", remindo_collection.id)

        self.db.session.flush()

    def add_usergroups(self):
        """
        Creates Groups for students
        """
        for course in self.courses:
            for i in self.group_ids:
                md.UserGroup.add_group(course=course, name="Group " + str(i))

    def link_users_to_courses(self):
        """
        Links users to their courses
        """
        # add faculty admins
        for admin_id in self.admin_ids:
            auth.add_user_role("local_" + admin_id, "admin", 1)

        # add students to courses
        for course in self.courses:
            for student in self.students:
                student.courses.append(course)
                auth.add_user_role(student.key, "student", course.collection_id)
                course_score = md.UserCourseScore(user_key=student.key, course_id=course.id)

        for student in self.students:
            self.db.session.add(md.Person(
                user_id=student.key,
                person_name=student.display_name))

        # add teachers to courses
        i = 0
        for course in self.courses:
            auth.add_user_role(self.teachers[i].key, "teacher", course.collection_id)
            i += 1
            if i >= len(self.teachers):
                i = 0

    def link_users_to_groups(self):
        """
        add students to random groups
        """
        for course in self.courses:
            for student in self.students:
                md.UserGroup.add_student(group=random.choice(course.groups), user=student)

    def add_mult_choice_exam(self, name, course, data, description=None, question_description=None):
        # add exams
        exam = md.Exam(title=name, course=course, type="multiple choice", visibility=True)
        exam.description = description
        exam.questions_description = question_description
        exam.start_time = datetime.datetime.now()
        exam.end_time = datetime.datetime.now() + datetime.timedelta(days=8)
        self.db.session.add(exam)

        questions = data.get("questions", dict())
        new_concepts = data.get("concepts", [])
        # concept_values = data.get("concept_values")

        # add concepts
        concepts = list()
        for name, study, mis, wght, maxs, mins, init in new_concepts:
            existing_concept = self.db.session.query(md.Concept).filter_by(name=name).first()
            if existing_concept and existing_concept in course.course_concepts:
                concepts.append(existing_concept)
            else:
                concepts.append(md.Concept(name=name, is_misconcept=mis, weight=wght))
        self.db.session.add_all(concepts)
        for concept in concepts:
            if concept not in course.course_concepts:
                course.course_concepts.append(concept)
        # course.course_concepts.extend(concepts)

        # add questions and answers
        questobjs = []
        for num, question in questions.items():
            quest = md.Question(
                remote_id="test_" + str(num),
                body=str(question['question']),
                type='multiple choice',
                exam=exam,
                number=num)
            for i, (key, answer) in enumerate(question['answers'].items()):
                text, concept_values = answer

                if key in question["correct"].split(","):
                    correct = True
                    score = 1
                else:
                    correct = False
                    score = 0
                ans = md.Answer(body=str(text), correct=correct, score=score, letter=chr(65 + i))
                quest.answers.append(ans)

                # add the concept values for the answer
                for concept_value in concept_values:
                    concept_id, value = concept_value
                    self.db.session.add(md.ConceptValue(value=value, concept=concepts[concept_id], answer=ans))

            update_question_max_score(quest)
            questobjs.append(quest)
        self.db.session.add_all(questobjs)

        self.add_results(exam)

    def add_results(self, exam):
        """
        Generates random answers for all students
        """
        for student in exam.course.users:
            if random.randint(0, 100) > self.participation_rate:
                continue
            person = md.Person.query.\
                filter(md.Person.user_id == student.key).one_or_none()
            if person is None:
                continue
            # Each student is given a random skill per exam: the likelihood that the student knows the answer to the
            # question.
            skill = random.randint(30, 100)
            exam_result = md.ExamResult(exam_id=exam.id, person_id=person.id)
            more_answers = random.randint(0, 10)
            for question in exam.questions:
                if more_answers < 1:
                    answer_count = random.randint(1, len(question.answers.all()) // 2)
                    ans = random.sample([i for i in range(len(question.answers.all()))], answer_count)

                    answer_body = "{"
                    for a in ans:
                        answer_body += chr(a + 65) + ","
                    if len(answer_body) > 1:
                        answer_body = answer_body[:-1] + "}"
                    else:
                        answer_body += "}"

                    correct_answers = []
                    for i, answer in enumerate(question.answers.all()):
                        if answer.correct:
                            correct_answers.append(i)

                    score = 0
                    for a in ans:
                        if a in correct_answers:
                            score += 1
                    score /= len(correct_answers)

                    question_result = md.QuestionResult(exam_result=exam_result,
                                                        question_id=question.id,
                                                        given_answer_id=None,
                                                        given_answer_body=answer_body,
                                                        score=score)
                elif random.randint(0, 100) < skill:
                    ans = random.choice(question.answers.filter(md.Answer.correct).all())
                    question_result = md.QuestionResult(exam_result=exam_result,
                                                        question_id=question.id,
                                                        given_answer_id=ans.id,
                                                        score=ans.score)
                else:
                    ans = random.choice(question.answers.all())
                    question_result = md.QuestionResult(exam_result=exam_result,
                                                        question_id=question.id,
                                                        given_answer_id=ans.id,
                                                        score=ans.score)

                self.db.session.add(question_result)
                self.db.session.flush()
                # update_question_score(question_result)

            # update_exam_score(exam_result)
            self.db.session.add(exam_result)
            self.db.session.flush()
            # exam_result.update_scores()
        # for concept in exam.concepts:
            # concept.update_scores(exam.course_id)
            # concept.update_scores_exam(exam.id)

        for question in exam.questions:
            update_p_value(question)
            update_std_value(question)
            update_rit_value(question)
            update_rir_value(question)
        # exam.update_concept_scores()

    def add_concept_model(self):
        from learnlytics.database.construct.construct import ConstructModel

        self.model = ConstructModel(name="Mock Model", method="mean_model", collection_id=self.courses[0].collection_id)
        self.db.session.add(self.model)
