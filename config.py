import os
from datetime import timedelta
from ldap3 import ALL
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    # Application root path (use APP_STATIC)
    APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/learnlytics"


class TestingConfig(BaseConfig):
    TESTING = True
    if os.getenv("CI"):
        SQLALCHEMY_DATABASE_URI = "postgres://testuser:testpass@postgres/backend_testdb"
    else:
        SQLALCHEMY_DATABASE_URI = "postgresql://localhost/backend_testdb"

    # General API
    SECRET_KEY_GENERAL_API = "thisisatestkey"

    # CSV importer
    RESTPLUS_VALIDATE = False
    UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/uploads/test"
    ALLOWED_EXTENSIONS = ['csv']

    # Authentication
    SECRET_KEY = "1234"
    JWT_AUTH_CLASS_KEY = "idp"
    JWT_AUTH_DEFAULT_IDP = "externalLDAPserver"
    JWT_DEFAULT_REALM = "T"
    IDENTITY_PROVIDERS = {
        'Local': {
            'local': {

            }
        },
        'LDAP': {
            'solisuu': {
                "FULL_NAME": "UU SOLISCOM LDAP Server",
                "IMAGE": None,
                'ADDRESS': 'soliscom.uu.nl',
                'USE_SSL': True,
                'GET_INFO': ALL,
                'USERNAME_TEMPLATE': 'SOLISCOM\\{}',
                'BASE_DN': 'DC=soliscom,DC=uu,DC=nl'
            }
        },
        'SAML': {

        },
        'OAuth': None
    }


class ProductionConfig(BaseConfig):
    # Flask
    FLASK_DEBUG = os.getenv("FLASK_DEBUG") == "1"
    FLASK_ENV = os.getenv("FLASK_ENV")

    # JWT Tokens
    SECRET_KEY = os.getenv("JWT_LOGIN_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRATION_IN_MINUTES", "60")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRATION_IN_MINUTES", "1440")))

    # Language settings
    LANGUAGE = 'nl'

    # Authentication Manager
    JWT_AUTH_CLASS_KEY = 'idp'
    JWT_AUTH_DEFAULT_IDP = "local"
    PROPAGATE_EXCEPTIONS = True  # 401 status for expired token

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/api/authentication/refresh'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE') == "True"
    JWT_CSRF_IN_COOKIES = False
    JWT_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
    JWT_COOKIE_DOMAIN = os.getenv("DOMAIN_NAME", "127.0.0.1")

    IDENTITY_PROVIDERS = {
        'Local': {
            'local': {

            }
        },
        'SAML': {
            os.getenv('SAML_PROVIDER', "error"): {
                "HOST": os.getenv('SAML_AUTH_URL', "error"),
                "CLIENTID": os.getenv('SAML_CLIENT_ID', "error"),
                "CLIENTSECRET": os.getenv('SAML_CLIENT_SECRET', "error"),
                "REDIRECT_URI": os.getenv('SAML_REDIRECT_URI', "error")
            }
        },
        'OAuth': None
    }

    BASE_URL = os.getenv("DOMAIN_NAME", "error")
    PUBLIC_PORT_HTTPS = os.getenv("PUBLIC_PORT_HTTPS", "error")
    API_PUBLIC_POSTFIX = os.getenv("API_PUBLIC_POSTFIX", "error")
    DEFAULT_PROVIDER = 'local'
    AUTHORIZATION_ROOT_USER = 'local_root'
    UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/" + os.getenv("UPLOAD_FOLDER", "error")
    # upload size limit in bytes
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 0))

    # LRS
    XAPI_PUBLIC_POSTFIX = os.getenv("XAPI_PUBLIC_POSTFIX", "error")
    MONGO_URL = os.getenv("MONGO_URL", "error")
    MONGO_DB = os.getenv("MONGO_DB", "error")

    # Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_DIALECT = os.getenv('POSTGRES_DIALECT', "error")
    DATABASE_USERNAME = os.getenv('POSTGRES_USER', "error")
    DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD', "error")
    DATABASE_HOST = os.getenv('POSTGRES_HOST', "error")
    DATABASE_PORT = os.getenv('POSTGRES_PORT', "error")
    DATABASE_DATABASE = os.getenv('POSTGRES_DB', "error")
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        DATABASE_DIALECT, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_DATABASE)

    db_repository = "db_repository"
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, db_repository)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CAPTCHA
    CAPTCHA_SECRET = os.getenv("CAPTCHA_SECRET", "error")

    # HTTPS
    USE_SSL = os.getenv("USE_SSL") == "True"

    if USE_SSL:
        CERT_FILE = os.getenv("SSL_CERT")
        KEY_FILE = os.getenv("SSL_KEY")

    # Database queries. Set this to true to show all queries made to the postgres database. This can be used to diagnose
    # performance issues with too many queries.
    LOG_DB_QUERIES = os.getenv("LOG_DB_QUERIES") == "True"

    # Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_IMPORTS = ["learnlytics.tasks"]
    CELERY_TIMEZONE = os.getenv("TIMEZONE")


conf = {
    "Production": ProductionConfig,
    "Testing": TestingConfig
}


def get_config(env_config=os.getenv('BACKEND_CONFIG', "Production")):
    """
    Returns the configuration linked to the string in LEARNLYTICS_CONFIG environment variable
    """
    return conf[env_config]
