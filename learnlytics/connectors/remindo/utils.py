"""
This module contains various utility functions to be used in the Remindo connector
"""

from collections import OrderedDict
import hashlib
import hmac
import json
import time
import socket
from urllib.parse import urlparse
from datetime import datetime
import pytz


def json_dumps(data):
    """
    A version of json.dumps that removes all whitespace
    :param data: data
    :return: data without whitespaces
    """
    separators = (',', ':')
    return json.dumps(data, separators=separators)


def to_php_dict(data):
    """
    A utility function that allows us to generate PHP dicts from python dicts
    :param data: Python dict
    :return: PHP dict
    """
    if data == {}:
        return []
    else:
        return data


def create_package(params, uuid, secret, rem_ip):
    """
    Creates a remindo-compatible package. Which is the params, combined
    with a sha-sum and an envelope.
    :param params: the params to wrap
    :param uuid: The uuid of the Remindo environment
    :param secret: The secret of the Remindo environment
    :param rem_ip: The ip address wanting to connect to the Remindo environment
    :return: a remindo packet
    """
    timestamp = int(time.time())
    data = OrderedDict([
        ('envelope', OrderedDict([
            ('uuid', uuid),
            ('timestamp', timestamp)
        ])),
        ('payload', json_dumps(to_php_dict(params))),
    ])

    data['signature'] = create_signature(data, secret, rem_ip)

    return data


def create_signature(data, secret, rem_ip=None):
    """
    Given a payload, creates a SHA-1 signature
    :param data: The data to create a signature for
    :param secret: The secret of the Remindo environment
    :param rem_ip: The ip address wanting to connect to the Remindo environment
    :return: the signed data
    """
    payload = json_dumps(data).replace("/", "\\/")
    if rem_ip is None:
        message = bytes(payload, "utf-8")
    else:
        message = bytes('{}:{}'.format(rem_ip, payload), "utf-8")

    digest = hmac.new(
        secret.encode("utf-8"),
        message,
        digestmod=hashlib.sha512
    ).hexdigest()
    return digest


def verify_signature(message, secret, url, given_signature):
    json_dict = message

    # determine ip address of server where the call was made to
    parsed_uri = urlparse(url)
    rem_domain = '{uri.netloc}'.format(uri=parsed_uri)
    rem_ip = socket.gethostbyname(rem_domain)

    # the given ip address
    given_ip = json_dict["envelope"]["address"]

    # check timestamp for 30 second timeframe
    if abs(json_dict["envelope"]["timestamp"] - int(time.time())) > 30:
        print("Timestamp does not fall in required window")
        return False

    data = OrderedDict([
        ('envelope', OrderedDict([
            ('timestamp', json_dict["envelope"]["timestamp"]),
            ('address', json_dict["envelope"]["address"]),
            ('callback', json_dict["envelope"]["callback"]),
            ('api_version', json_dict["envelope"]["api_version"]),
            ('encrypted', json_dict["envelope"]["encrypted"])
        ])),
        ('payload', json_dict["payload"])
    ])

    if hmac.compare_digest(given_signature, create_signature(data, secret, rem_ip)):
        return True
    if hmac.compare_digest(given_signature, create_signature(data, secret, given_ip)):
        return True
    if hmac.compare_digest(given_signature, create_signature(data, secret)):
        return True

    return False


def get_recipe_id(exam):
    return int(exam.remote_id.split("_")[-1].split("/")[0])


def get_moment_id(exam):
    return exam.properties["remindo"]["moments"][0]


def time_from_string(time):
    """
    Takes a string that was returned from Remindo and creates a timezone aware python date object
    """
    remindo_dateformat = "%Y-%m-%d %H:%M:%S"
    remindo_timezone = "Europe/Amsterdam"

    time = datetime.strptime(time, remindo_dateformat)
    timezone = pytz.timezone(remindo_timezone)
    time_aware = timezone.localize(time)

    return time_aware


def get_lrs_actor(base_url, user_id):
    actor = {
        "homePage": f"{base_url}/users",
        "name": str(user_id)
    }

    return actor


def get_object_id(base_url, activity):
    if activity.type.name == "exam":
        recipe_id = get_recipe_id(activity)
        return f"{base_url}/exams/{recipe_id}"
    elif activity.type.name.startswith("question"):
        item_identifier = activity.remote_id.split("_")[-1]
        return f"{base_url}/items/{item_identifier}"
