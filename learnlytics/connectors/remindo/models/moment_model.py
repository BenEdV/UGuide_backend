
"""
Contains the RemindoMomentModel, which handles all request related to recipes.
"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from datetime import datetime
import time
import pytz

from learnlytics.connectors.remindo.models import RemindoSubModel
from learnlytics.connectors.remindo.utils import time_from_string

from learnlytics.tasks.exam import load_results


class RemindoMomentModel(RemindoSubModel):
    """
    Handle all requests related to moments
    """

    def get_moments(self):
        """
        Returns all moments.
        :return: A list of moments.
        """
        data = self.connector.moment_list()
        return data

    def get_moment(self, moment_id):
        """
        Return the moment with the given id
        """
        params = {
            "ids": moment_id
        }
        data = self.connector.moment_list(params)
        return data["moments"][str(moment_id)]

    def get_moments_for_recipe(self, recipe_id):
        """
        Returns a list of moments for the given recipe id
        """
        params = {"recipe_ids": recipe_id}
        data = self.connector.moment_list(params)
        moments = []
        if data["moments"] == []:
            # if there are no moments Remindo returns an empty array, if there are it returns a dictionary
            return moments

        for remindo_moment in data["moments"].values():
            moments.append({
                "id": remindo_moment["id"],
                "name": remindo_moment["name"],
                "time_start": time_from_string(remindo_moment["time_start"]),
                "time_end": self.get_moment_end_time(remindo_moment)
            })
        return moments

    def determine_moment_for_exam(self, collection, exam):
        recipe_id = exam.remote_id.split("_")[1].split("/")[0]
        moments = self.get_moments_for_recipe(recipe_id)

        if moments == []:
            # There are no moments for the exam
            return

        if len(moments) == 1:
            self.attach_moment_to_exam(exam, moments[0]["id"])
            return

        import operator
        moments.sort(key=operator.itemgetter('time_end'), reverse=True)

        for moment in moments:
            if collection.course_instance is None:
                return
            period = collection.course_instance.period
            if period.start_date <= moment["time_start"].date() and period.end_date >= moment["time_end"].date():
                self.attach_moment_to_exam(exam, moment["id"])
                return

        # If no matching moment is found attach to latest moment
        self.attach_moment_to_exam(exam, moments[0]["id"])

    def attach_moment_to_exam(self, exam, moment_id):
        moment = self.get_moment(moment_id)

        exam.start_time = time_from_string(moment["time_start"])
        exam.end_time = self.get_moment_end_time(moment)

        # Set up automatic result loading
        if exam.properties["remindo"].get("import_results_on_close", False):
            load_results.apply_async(args=[exam.id], eta=exam.end_time)

    def get_moment_end_time(self, moment):
        if moment["time_end"]:
            return time_from_string(moment["time_end"])
        else:
            return time_from_string(moment["time_start"]) + timedelta(minutes=moment["duration"])
