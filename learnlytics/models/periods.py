# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project period (3 4)
# (C) Copyright Utrecht University (Department of Information and Computing Sciences)
"""
This module contains the model for periods
"""

from learnlytics.authentication.util import current_identity
from learnlytics.authorization.manager import authorize
from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.user import UserRole
from learnlytics.extensions import db
import learnlytics.database.studydata as md


# pylint: disable=no-member
class Periods(object):  # pylint: disable=no-init
    """
    This class contains methods to get, add delete periods
    """

    @staticmethod
    def get_period(period_id):
        """
        Gets a period with the given period_id.
        :param period_id: id of the the period to get
        :return: a json of the requested period.
        """
        period = md.Period.get(period_id, required=True)
        result_dic = Periods._period_dict(period)
        return result_dic

    @staticmethod
    def _period_dict(period):
        return {
            "id": period.id,
            "name": period.name,
            "start_date": period.start_date.isoformat() if period.start_date else None,
            "end_date": period.end_date.isoformat() if period.end_date else None,
            "instances_count": period.instances.count()
        }

    @staticmethod
    def get_periods():
        """
        Gets a list of all available periods.
        :return: a list of json objects of all the available periods.
        """
        periods = md.Period.query.all()
        result = []
        for period in periods:
            period_dict = Periods._period_dict(period)
            result.append(period_dict)
        return result

    @staticmethod
    def add_period(name, start_date, end_date):
        """
        Adds a new period to the database
        """
        period = md.Period(
            name=name,
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(period)
        db.session.commit()

    @staticmethod
    def delete_period(period):
        """
        Deletes a period with the given period_id.
        :param period: The period to delete.
        """
        db.session.delete(period)
        db.session.commit()
