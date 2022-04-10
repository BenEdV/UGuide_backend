"""
This module defines database object and init and migration functions
"""
from learnlytics.extensions import db


def add_default_rows():
    """
    Adds the default types, permissions and roles. This is to be run when the system is started so that any changes will
    be immediately updated
    """
    from learnlytics.database.authorization.permission import Permission
    from learnlytics.database.authorization.role import Role, RolePermission
    from learnlytics.database.construct.construct import ConstructType, ConstructRelationType, \
        ConstructActivityRelationType
    from learnlytics.database.studydata.activity import ActivityType, ActivityRelationType

    activity_type_names = [
        "exam", "survey", "comment", "question.open", "question.multiple_choice", "question.multiple_selection",
        "question.likert", "material.book.book", "material.book.chapter", "material.file.factsheet",
        "material.file.slides", "material.article.article", "material.video.unspecified",
        "material.article.wikipedia", "material.video.youtube", "material.video.hvp"]
    activity_relation_type_names = ["exam_question", "exam_comment", "book_chapter"]
    construct_type_names = ["concept", "misconception", "positive_trait", "negative_trait"]
    construct_relation_type_names = ["meronomical", "prerequisite_outcome", "taxonomical", "concept_misconception"]
    construct_activity_relation_type_names = ["tests", "exhibits", "teaches", "remedies"]
    permission_names = [
        "see_own_results", "see_aggregated_results", "see_user_results", "see_anonymized_user_results",
        "see_collection", "manage_collection",
        "see_permissions", "manage_permissions", "see_roles", "manage_roles",
        "see_collection_user_roles", "manage_collection_user_roles", "manage_users",
        "see_periods", "manage_periods",
        "see_users", "see_all_courses", "manage_courses", "see_courses",
        "use_dev_calls", "generate_api_key",
        "invalidate_cache", "reset_user_password", "see_usage_report",
        "see_constructs", "manage_constructs",
        "manage_construct_models", "see_construct_models",
        "see_activities", "see_invisible_activities", "manage_activities", "load_activity_results",
        "see_connectors",
        "see_main_lrs_write_key", "see_sec_lrs_write_key", "see_sec_lrs_read_key", "manage_sec_lrs"
    ]
    # These roles are hardcoded, other roles can be added by admins
    role_names = ["member", "student", "teacher", "admin", "manager", "developer", "teaching_assistant", "researcher"]
    # member is a special role. It denotes which users (usually students) are to be used to determine an average of
    # a collection
    default_role_permissions = {
        "member": [],
        "student": [
            "see_own_results", "see_aggregated_results", "see_collection",
            "see_constructs", "see_anonymized_user_results",
            "see_courses", "see_activities"],
        "teacher": [
            "see_own_results", "see_user_results", "see_aggregated_results", "see_anonymized_user_results",
            "see_collection_user_roles",
            "see_collection", "manage_collection", "see_all_courses", "see_periods",
            "see_users", "manage_users",
            "see_courses", "manage_courses",
            "see_activities", "see_invisible_activities", "manage_activities", "load_activity_results",
            "see_constructs", "manage_constructs",
            "see_construct_models", "manage_construct_models",
            "see_connectors",
            "see_main_lrs_write_key", "see_sec_lrs_write_key", "see_sec_lrs_read_key", "manage_sec_lrs"],
        "admin": [
            "see_collection", "manage_collection",
            "see_roles", "manage_roles", "see_collection_user_roles", "manage_collection_user_roles",
            "see_all_courses", "manage_courses", "generate_api_key",
            "see_periods", "manage_periods",
            "reset_user_password", "see_usage_report",
            "see_activities", "see_invisible_activities", "manage_activities", "load_activity_results",
            "manage_construct_models", "see_construct_models", "see_users", "manage_users",
            "see_connectors",
            "see_main_lrs_write_key", "see_sec_lrs_write_key", "see_sec_lrs_read_key", "manage_sec_lrs"],
        "manager": [
            "see_own_results", "see_user_results", "see_aggregated_results",
            "manage_collection", "see_collection",
            "see_roles",
            "manage_roles",
            "see_collection_user_roles", "manage_collection_user_roles", "see_courses"],
        "developer": [
            "use_dev_calls", "invalidate_cache", "see_permissions", "manage_permissions"],
        "teaching_assistant": [],
        "researcher": []
    }

    activity_types = []
    activity_relation_types = []
    construct_types = []
    construct_relation_types = []
    construct_activity_relation_types = []
    permissions = []
    roles = []
    role_permissions = []

    for activity_type_name in activity_type_names:
        activity_type = ActivityType.query.filter(ActivityType.name == activity_type_name).one_or_none()
        if activity_type is None:
            activity_types.append(ActivityType(name=activity_type_name))

    for activity_relation_type_name in activity_relation_type_names:
        activity_relation_type = ActivityRelationType.query.filter(
            ActivityRelationType.name == activity_relation_type_name).one_or_none()
        if activity_relation_type is None:
            activity_relation_types.append(ActivityRelationType(name=activity_relation_type_name))

    for construct_type_name in construct_type_names:
        construct_type = ConstructType.query.filter(ConstructType.name == construct_type_name).one_or_none()
        if construct_type is None:
            construct_types.append(ConstructType(name=construct_type_name))

    for construct_relation_type_name in construct_relation_type_names:
        construct_relation_type = ConstructRelationType.query.filter(
            ConstructRelationType.name == construct_relation_type_name).one_or_none()
        if construct_relation_type is None:
            construct_relation_types.append(ConstructRelationType(name=construct_relation_type_name))

    for construct_activity_relation_type_name in construct_activity_relation_type_names:
        construct_activity_relation_type = ConstructActivityRelationType.query.filter(
            ConstructActivityRelationType.name == construct_activity_relation_type_name).one_or_none()
        if construct_activity_relation_type is None:
            construct_activity_relation_types.append(
                ConstructActivityRelationType(name=construct_activity_relation_type_name))

    for permission_name in permission_names:
        permission = Permission.query.filter(Permission.name == permission_name).one_or_none()
        if permission is None:
            permissions.append(Permission(name=permission_name))

    for role_name in role_names:
        role = Role.query.filter(Role.name == role_name).one_or_none()
        if role is None:
            role = Role(name=role_name)
            roles.append(role)
        role.permissions = []

    db.session.add_all(activity_types)
    db.session.add_all(activity_relation_types)
    db.session.add_all(construct_types)
    db.session.add_all(construct_relation_types)
    db.session.add_all(construct_activity_relation_types)
    db.session.add_all(permissions)
    db.session.add_all(roles)
    db.session.flush()

    for role_name, permission_names in default_role_permissions.items():
        role = Role.query.filter(Role.name == role_name).one_or_none()
        if role is None:
            raise Exception(f"Role {role_name} does not exists")

        for permission_name in permission_names:
            permission = Permission.query.filter(Permission.name == permission_name).one_or_none()
            if permission is None:
                raise Exception(f"Permission {permission_name} does not exists")
            role_permissions.append(RolePermission(permission_id=permission.id, role_id=role.id))

    db.session.add_all(role_permissions)

    print(f"Updating default database rows. {len(activity_types)} new activity types, {len(activity_relation_types)} new activity relation types, {len(construct_relation_types)} new construct relation types, {len(construct_types)} new construct types, {len(construct_activity_relation_types)} new construct-activity relation types, {len(permissions)} new permissions, {len(roles)} new roles, {len(role_permissions)} role permissions. ")  # noqa
    db.session.commit()
    print("Updated default database rows")
