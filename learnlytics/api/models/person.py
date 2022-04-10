from flask_restplus import abort

from learnlytics.extensions import db
import learnlytics.database.studydata as md


class PersonModel(object):
    """
    Model to add a result
    """

    @staticmethod
    def add_person(data, source):
        """
        Adds a user with the given information.
        Required:
            remote_user_id
        Optional
            name
            mail
            role
            institution_id
        """
        if "remote_user_id" not in data:
            abort(409, "Remote User ID not found by person with data: {}".format(data))

        result = {
            "already_exists": False,
            "linked": False
        }

        person_remote_id = source + "_" + str(data["remote_user_id"])

        person = md.Person.get_from_remote_id(person_remote_id)
        if person is not None:
            result["already_exists"] = True
            person.display_name = data.get("name")
            person.role = data.get("role")
            person.mail = data.get("mail")
            person.institution_id = data.get("institution_id")
        else:
            person = md.Person(
                remote_id=person_remote_id,
                display_name=data.get("name"),
                role=data.get("role"),
                mail=data.get("mail"),
                institution_id=data.get("institution_id"))
            db.session.add(person)
            db.session.flush()

        if person.user is None:
            result["linked"] = PersonModel.link_person_to_user(person)
        else:
            result["linked"] = True

        db.session.commit()

        return result

    @staticmethod
    def link_person_to_user(person):
        # Find link candidates
        candidates = []
        if person.display_name:
            candidates.extend(md.User.query.filter(md.User.display_name == person.display_name).all())

        if person.mail:
            candidates.append(md.User.query.filter(md.User.mail == person.mail).one_or_none())

        if person.institution_id:
            candidates.append(md.User.query.filter(md.User.institution_id == person.institution_id).one_or_none())

        # Attempt link
        # filter nones out
        candidates = [c for c in candidates if c is not None]
        # filter duplicates out
        ids = []
        old_candidates = candidates
        candidates = []
        for candidate in old_candidates:
            if candidate.id not in ids:
                ids.append(candidate.id)
                candidates.append(candidate)

        if candidates == []:
            print("No candidates")
            return False
        if len(candidates) > 1:
            print("Multiple candidates found")
            return False

        person.user = candidates[0]
        return True

    @staticmethod
    def add_persons(data, source):

        result = {
            "new": 0,
            "linked": 0,
            "total": 0,
            "unlinked": []
        }

        for person_data in data:
            res = PersonModel.add_person(person_data, source)
            result["total"] += 1
            if not res["already_exists"]:
                result["new"] += 1
            if res["linked"]:
                result["linked"] += 1
            else:
                result["unlinked"].append(person_data)

        return result
