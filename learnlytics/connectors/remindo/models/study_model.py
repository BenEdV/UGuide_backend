"""
This module has the model for a Remindo study
"""

from learnlytics.connectors.remindo.models import RemindoSubModel


class RemindoStudyModel(RemindoSubModel):
    """
    The model for a Remindo study with functions on studies
    """
    def get_studies(self, study_id=None):
        """
        Get a (list of) study (studies) from Remindo
        :param study_id: (int, optional, default None) id of the study.
        :return: A list containing studies.
        """
        params = {}
        if study_id:
            params["study_id"] = study_id
        data = self.connector.study_list(params)
        studies = []
        for study_data in data["studies"].values():
            studies.append({"id": study_data['id'],
                            "name": study_data["name"],
                            "code": study_data["code"]})
        return studies
