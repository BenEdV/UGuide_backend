#!/bin/bash

if [ ! -d log ]; then
	echo "Making log directory"
	mkdir log
fi

echo "Starting updater..."
./update.py

echo "Starting Celery task worker..."
celery -A learnlytics.app:celery worker --loglevel=DEBUG --logfile="log/celery.log" --detach --pidfile=''
# celery -A learnlytics.app:celery control enable_events

if [ "$FLASK_ENV" == "development" ]
then
	echo "Starting flask debug runner..."
	./main.py
else
	echo "Starting UWSGI..."
	uwsgi settings.ini
fi
