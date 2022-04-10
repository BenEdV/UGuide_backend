#!/bin/bash
pylint main learnlytics mock_data config create_api create_metadb
# Give exit code 1 (fail) only if there is a fatal error
exit $((1&$?))
