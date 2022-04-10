#!/usr/bin/env python3
"""
Main file containing the run script for the application
"""
import logging
import logging.config
import sys
import yaml

from learnlytics.app import app
from learnlytics.database import add_default_rows
from config import get_config

import warnings

if __name__ == '__main__':
    # Silence benign warnings
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")

    logging.config.dictConfig(yaml.safe_load(open('logging.conf')))

    config_obj = get_config()
    if config_obj.LOG_DB_QUERIES:
        db_logger = logging.getLogger("sqlalchemy.engine")
        db_logger.setLevel(logging.INFO)

    if config_obj.USE_SSL:
        context = (config_obj.CERT_FILE, config_obj.KEY_FILE)
        app.run(
            debug=config_obj.FLASK_DEBUG,
            use_reloader=True,
            threaded=True,
            host="0.0.0.0",
            port=80,
            ssl_context=context)
    else:
        app.run(
            debug=config_obj.FLASK_DEBUG,
            use_reloader=True,
            threaded=True,
            host="0.0.0.0",
            port=80)
    add_default_rows()
