FROM python:3.8

WORKDIR /var/uwsgi

# Install requirements
RUN pip install uwsgi
ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD . /var/uwsgi

# Add user so that uWSGI doesn't run as root
# RUN useradd --system -s /sbin/nologin uwsgi
# USER uwsgi

EXPOSE 80

ENTRYPOINT ["./docker-entrypoint.sh"]
