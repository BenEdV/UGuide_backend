"""
This file extends the functionality of datetime
"""

from datetime import datetime


def strptime_frontend(date_string):
    date_string = date_string.replace("Z", "+00:00")
    return datetime.fromisoformat(date_string)
