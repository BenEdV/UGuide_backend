"""
This file is the core module of the application. It contains the system object itself
and several options
"""
from flask import Flask

from config import get_config
from learnlytics.extensions import celery, db
from learnlytics.util.json import JsonExtendEncoder


def create_minimal_app(config_obj=None):
    """
    Function that creates minimal flask application and loads the configuration object.
    :param config_obj:  Config object/module
    :return: Flask application object
    """
    app = Flask(__name__)

    if config_obj:
        app.config.from_object(config_obj)
    app.json_encoder = JsonExtendEncoder

    return app


def create_app():
    """
    Function that creates flask application object and loads and links all plugins, models and api routes
    :return: Flask application object
    """
    config_obj = get_config()
    app = create_minimal_app(config_obj)

    # load authentication module
    from learnlytics.database.authorization.user import load_user, add_user, payload_ext
    from learnlytics.authentication import AuthenticationManager
    AuthenticationManager(None, app, load_user, add_user, payload_ext)

    create_api(app)

    # initialize extensions
    db.init_app(app)
    celery.init_app(app)

    app.jinja_env.globals["BASE_URL"] = config_obj.BASE_URL

    from flask import jsonify, request
    from learnlytics.authentication.util import current_identity
    from learnlytics.database.learnlyticslogging.requestlog import RequestLog
    import datetime

    @app.after_request
    def after_request(response):
        """
        Hook into all requests to log backend requests in the database
        """
        user = current_identity()
        if user:
            requestlog = RequestLog(
                user_id=user.id,
                time=datetime.datetime.now(),
                request_path=request.path,
                request_method=request.method)
            db.session.add(requestlog)
            db.session.commit()
            return response

        if request.path != "/currentuser/authentication" or response.status != "200 OK":
            return response

        data = request.get_json()
        if data is None:
            return response

        if "username" not in data:
            return response

        from learnlytics.database.authorization.user import load_user
        user = load_user(data["username"])

        if user is None:
            return response

        requestlog = RequestLog(
            user_id=user.id,
            time=datetime.datetime.now(),
            request_path=request.path,
            request_method=request.method)
        db.session.add(requestlog)
        db.session.commit()
        return response

    return app


def create_api(app):  # pylint: disable=too-many-locals
    """
    Connects the API resources to routes and the flask App.
    """
    # Build statements for Swagger
    import learnlytics.resources

    # register blueprints
    from create_api import api, learnlytics_blueprint, connector_blueprint, general_api_blueprint, widget_blueprint
    app.register_blueprint(learnlytics_blueprint)
    app.register_blueprint(connector_blueprint)
    app.register_blueprint(general_api_blueprint)
    app.register_blueprint(widget_blueprint)


app = create_app()
