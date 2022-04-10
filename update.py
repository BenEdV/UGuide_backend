#!/usr/bin/env python3
"""
This file should be run before the application is started to ensure that the database is available and the database
contents are in agreement with the expectations of the backend
"""
import psycopg2
import time
import logging
import logging.config
import yaml

from config import get_config
from learnlytics.app import create_app
from learnlytics.database import add_default_rows

logging.config.dictConfig(yaml.safe_load(open('logging.conf')))

logger = logging.getLogger('console')
config_obj = get_config()

while(True):
    try:
        conn = psycopg2.connect(config_obj.SQLALCHEMY_DATABASE_URI)
        logger.info("Postgres connection established")
        break
    except:  # noqa
        time.sleep(1)
        logger.info("Waiting for postgres...")

app = create_app()
app.app_context().push()

if __name__ == "__main__":
    """
    Run this scripts to add the default rows to the database. Docker can use this as uwsgi does not run main.py
    """
    if config_obj.FLASK_ENV != "development":
        print("Updating Database")
        add_default_rows()
