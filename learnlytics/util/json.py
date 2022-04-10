"""
This file extends the functionality of json
"""

import json
from datetime import date
from datetime import datetime


class JsonExtendEncoder(json.JSONEncoder):
    """
    This class provide an extension to json serialization for datetime/date.
    """

    def default(self, obj):
        """
        provide a interface for datetime/date
        """
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)
