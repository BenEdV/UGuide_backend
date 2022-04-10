
# pylint: skip-file

"""
Contains the exam-data for the meta-database
"""

import random
import datetime
import json
import sys

from learnlytics.analyse.question_value import update_p_value, update_std_value, update_rit_value, update_rir_value
from learnlytics.analyse.exam import update_exam_score, update_exam_max_score
from learnlytics.analyse.question import update_question_score, update_question_max_score
from learnlytics.api.models.authorization import add_api_key_permission
import learnlytics.authorization.manager as auth
from learnlytics.database.api.apikey import APIKey
import learnlytics.database.studydata as md
from learnlytics.database.api.apikey import APIKeyPermission, PermissionGenAPI
from learnlytics.database.authorization.user import User, UserPassHash
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.role import Role
from learnlytics.database.authorization import init_authorization_db
from learnlytics.database.api import add_gen_api_permissions

# from mock_data.create_survey import MockSurvey

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


class MockDatabase(object):  # pylint: disable=too-few-public-methods, missing-docstring
    def __init__(self, db):
        """
        Initiate the mockdatabase with given database and app
        :param db: database
        :param app: app
        """
        self.db = db
        # self.auth = get_auth_manager()
        self.passwords = dict()
        self.faculties = list()
        self.courses = list()
        self.course_instances = list()
        self.studies = list()
        self.root = list()
        self.admins = list()
        self.teachers = list()
        self.students = list()
        self.participation_rate = 100

    def fill_data(self, num_students=40, num_groups=4, participation_rate=100):
        """
        Fills the database with the data of the mock-exam
        """
        # pylint: disable=too-many-statements
        if not Role.get_name("student", required=False):
            print("No roles were found. First run ./create_metadb.py")
            sys.exit(1)

        self.root_ids = range(1, 2)
        self.admin_ids = range(2, 4)
        self.teacher_ids = range(4, 8)
        self.student_ids = range(8, 8 + num_students)
        self.all_ids = range(1, 8 + num_students)

        self.participation_rate = participation_rate
        self.general_api_key = ""

        self.course_info = [
            {"name": "Biologie en ecologie van planten", "code": "B-B1BEP13"},
            {"name": "Moleculaire biologie", "code": "B-B1MB05"},
            {"name": "Systeembiologie", "code": "B-B1SYSB09"},
            {"name": "Biologie van dieren", "code": "B-B1DIER05"},
            {"name": "Experiment en statistiek", "code": "B-B1EXST13"}
        ]

        self.group_ids = range(1, num_groups + 1)

        print("Adding users...")
        self.add_users()
        print("Creating collection hierarchy...")
        self.add_collection_tree()
        self.add_course_collections()
        self.add_group_collections()
        print("Add general api keys and permissions")
        self.add_root_api_key()
        self.add_general_api_permissions()
        print("Linking users to courses...")
        self.link_users_to_collection()
        self.add_concept_model()

        # mockSurvey = MockSurvey(db=self.db)
        # mockSurvey.create_survey()
        from learnlytics.api.models.exams import Exams as ExamModel
        from learnlytics.api.models.result_model import Result as ResultModel
        from learnlytics.api.models.person import PersonModel

        exam_model = ExamModel()
        result_model = ResultModel()
        person_model = PersonModel()

        # with open("mock_data/exams/mock_exam1.json") as exam_file:
        #     exam1 = exam_model.add_exam(md.Course.get_code("B-B1MB05"), json.load(exam_file), "Mock")

        # with open("mock_data/exams/mock_exam2.json") as exam_file:
        #     exam2 = exam_model.add_exam(md.Course.get_code("B-B1MB05"), json.load(exam_file), "Mock")

        # with open("mock_data/persons/persons_10_ind_8.json") as persons_file:
        #     person_model.add_persons(json.load(persons_file), "Mock")

        # with open("mock_data/results/mock_exam1_results_10_ind_8.json") as results_file:
        #     result_model.add_results(json.load(results_file), exam1, "Mock")

        # with open("mock_data/results/mock_exam2_results_10_ind_8.json") as results_file:
        #     result_model.add_results(json.load(results_file), exam2, "Mock")

        print("Committing to database...")
        self.db.session.commit()
        # Removes the session

        self.db.session.remove()

    def add_general_api_permissions(self):
        add_gen_api_permissions()

        def add_permission(api_key, permission_string, collection):
            permission = PermissionGenAPI.query.filter(PermissionGenAPI.name == permission_string).one()

            key_permission = APIKeyPermission(
                api_key=self.api_key,
                permission=permission,
                collection=collection)
            self.db.session.add(key_permission)

        add_permission(self.api_key, "add_person", self.beta)
        add_permission(self.api_key, "add_exam", self.beta)
        add_permission(self.api_key, "add_exam_result", self.beta)

    def add_root_api_key(self):
        self.api_key = APIKey.add_api_key(self.general_api_key, "root")

    def add_collection_tree(self):
        self.beta = Collection(name="Betawetenschappen", parent_id=1)
        self.bio = Collection(name="Biologie", parent=self.beta)

        self.db.session.add_all([self.beta, self.bio])

    def add_course_collections(self):
        end_date = datetime.date.today() + datetime.timedelta(days=80)

        period = md.Period(
            name="Period 1",
            start_date=datetime.date.today(),
            end_date=end_date
        )

        for course in self.course_info:
            self.courses.append(
                md.Course(
                    name=course["name"],
                    code=course["code"]
                )
            )
        self.db.session.add(period)
        self.db.session.add_all(self.courses)
        self.db.session.flush()

        for course in self.courses:
            self.course_instances.append(md.CourseInstance(
                course=course,
                period=period,
                parent_collection_id=self.bio.id
            ))

        self.db.session.add_all(self.course_instances)
        self.db.session.flush()

    def add_group_collections(self):
        self.group_collections = []
        for course_instance in self.course_instances:
            for group_index in self.group_ids:
                self.group_collections.append(
                    Collection(name=f"Group {group_index}", parent=course_instance.collection))
        self.db.session.add_all(self.group_collections)

    def add_users(self):
        """
        Add users with password test
        """
        for i in self.root_ids:
            self.root.append(User(
                "mock_" + str(i),
                names[i] + " " + last_names[i],
                names[i].lower() + "@test.com",
                names[i],
                last_names[i]))

        for i in self.admin_ids:
            self.admins.append(User(
                "mock_" + str(i),
                names[i] + " " + last_names[i],
                names[i].lower() + "@test.com",
                names[i],
                last_names[i]))

        for i in self.teacher_ids:
            self.teachers.append(User(
                "mock_" + str(i),
                names[i] + " " + last_names[i],
                names[i].lower() + "@test.com",
                names[i],
                last_names[i]))

        for i in self.student_ids:
            self.students.append(User(
                "mock_" + str(i),
                names[i] + " " + last_names[i],
                names[i].lower() + "@test.com",
                names[i],
                last_names[i]))

        self.db.session.add_all(self.root)
        self.db.session.add_all(self.admins)
        self.db.session.add_all(self.teachers)
        self.db.session.add_all(self.students)

        self.all_users = self.root + self.admins + self.teachers + self.students

        self.db.session.flush()

        for user in self.all_users:
            self.db.session.add(UserPassHash(user.id, "test"))

        self.db.session.flush()

    def link_users_to_collection(self):
        """
        Links users to their courses
        """
        from learnlytics.database.authorization.role import Role

        admin_role = Role.get_name("admin")
        member_role = Role.get_name("member")
        student_role = Role.get_name("student")
        teacher_role = Role.get_name("teacher")
        dev_role = Role.get_name("developer")

        # add faculty admins
        i = 0
        for fac in self.faculties:
            auth.add_user_role(self.admins[i].id, admin_role.id, self.beta.id)
            i += 1

        # add students to collection
        for student in self.students:
            for course_instance in self.course_instances:
                auth.add_user_role(student.id, student_role.id, course_instance.collection_id)
                auth.add_user_role(student.id, member_role.id, course_instance.collection_id)

            group_index = random.randint(1, 2)
            for group in self.group_collections:
                if group.name == f"Group {group_index}":
                    auth.add_user_role(student.id, student_role.id, group.id)
                    auth.add_user_role(student.id, member_role.id, group.id)

        # add teachers to collection
        for teacher in self.teachers:
            auth.add_user_role(teacher.id, teacher_role.id, self.beta.id)
            auth.add_user_role(teacher.id, teacher_role.id, 1) # become teacher for university collection too

            for course_instance in self.course_instances:
                auth.add_user_role(teacher.id, teacher_role.id, course_instance.collection_id)

            for group in self.group_collections:
                auth.add_user_role(teacher.id, teacher_role.id, group.id)

        # add dev role to 0000001
        auth.add_user_role(self.root[0].id, dev_role.id, 1)

    def add_concept_model(self):
        from learnlytics.database.construct.construct import ConstructModel

        self.model = ConstructModel(name="Mock Model", method="mean_model", collection_id=self.beta.id)
        self.db.session.add(self.model)
