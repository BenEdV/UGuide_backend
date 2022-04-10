"""
This Module contains the authorization manager
"""

from flask_restplus import abort

from learnlytics.authentication.util import current_identity

from learnlytics.database.authorization.collection import Collection
from learnlytics.database.authorization.user import UserRole, User
from learnlytics.database.authorization.role import Role, RolePermission
from learnlytics.database.authorization.permission import Permission
from learnlytics.extensions import db
from learnlytics.models.user_settings import CourseUserSettings as UserSettingsModel


def authorize(collection, permissions, user=None, do_abort=True):
    """
    Checks if the logged-in user has all the given permissions for the given collection
    """
    if not user:
        user = current_identity()
        if not user:
            if do_abort:
                abort(403, message="No user authenticated")
            return False

    user_permissions = get_user_permissions(collection.id, user.id)

    for permission in Permission.query.filter(Permission.name.in_(permissions)).all():
        if not permission:
            if do_abort:
                abort(404, message=f"No permission with name: {permission.name} found.")
            return False

        if permission not in user_permissions:
            if do_abort:
                abort(403, message=f"User {user.display_name} does not have permission {permission.name}.")
            return False

    return True


def get_user_roles(collection_id, user_id=None):
    """
    Gives a list of roles that a user has for a collection. By default the current user is tested.
    """
    if not user_id:
        user_id = current_identity().id

    roles = Role.query.join(UserRole, UserRole.role_id == Role.id).filter(
        UserRole.user_id == user_id,
        UserRole.collection_id == collection_id).all()

    return roles


def get_user_permissions(collection_id, user_id=None):
    """
    Gives a list of roles that a user has for a collection. By default the current user is tested.
    """
    if not user_id:
        user_id = current_identity().id

    permissions = Permission.query.\
        join(RolePermission, RolePermission.permission_id == Permission.id).\
        join(Role, Role.id == RolePermission.role_id).\
        join(UserRole, UserRole.role_id == Role.id).\
        filter(
            UserRole.user_id == user_id,
            UserRole.collection_id == collection_id
        ).all()

    return permissions


def add_permissions(permissions):
    """
    Adds the specified permissions into the database so they can be used by
    roles
    :permissions: An array of strings that are used as names for the permissions
    """
    for permission in permissions:
        p = Permission(name=permission)
        db.session.add(p)

    db.session.commit()


def delete_permissions(permissions):
    """
    Adds the specified permissions into the database so they can be used by
    roles
    :permissions: An array of strings that are used as names for the permissions
    """
    for permission_name in permissions:
        permission = Permission.query.filter(Permission.name == permission_name).one_or_none()
        db.session.delete(permission)

    db.session.commit()


def add_role(role_name, permissions):
    """
    Creates a new role with a set of permissions
    :role: Name of the role to be created
    :permissions: A list of strings corresponding to the permissions the role should have
    """
    role = Role(name=role_name)
    db.session.add(role)
    for permission_name in permissions:
        permission = Permission.query.filter(Permission.name == permission_name).one_or_none()
        if not permission:
            abort(404, message=_("No permission with name: %(permission_name)s found.") % {
                "permission_name": permission_name})
        role.permissions.append(permission)

    db.session.commit()
    return role.id


def remove_role(role):
    """
    Deletes a role from the database
    """
    db.session.delete(role)
    db.session.commit()


def change_role(role, permissions):
    """
    Changes a roles permissions to the list given
    """
    role.permissions = []
    for permission_name in permissions:
        permission = Permission.query.filter(Permission.name == permission_name).one_or_none()
        if not permission:
            abort(404, message=_("No permission with name: %(permission_name)s found.") % {
                "permission_name": permission_name})
        role.permissions.append(permission)

    db.session.commit()


def add_collection(name, parent_id=None, settings=None):
    """
    Creates a new collection
    """
    if settings is None:
        settings = {}

    collection = Collection(name=name, parent_id=parent_id, settings=settings)
    db.session.add(collection)
    db.session.commit()
    return collection


def remove_collection_with_name(name):
    """
    Creates a new collection
    """
    c = Collection.query.filter(Collection.name == name).one_or_none()
    db.session.delete(c)
    db.session.commit()


def remove_collection(collection):
    """
    Deletes a collection from the database
    """
    db.session.delete(collection)
    db.session.commit()


def change_collection(collection, data):
    parent_id = data.get("parent_id", None)
    name = data.get("name", None)
    settings = data.get("settings", None)
    if name:
        collection.name = name
    if parent_id:
        collection.parent_id = parent_id
    if settings:
        collection.settings = settings
    db.session.commit()
    return collection


def add_user_role(user_id, role_id, collection_id):
    """
    Gives a user a role for a collection
    """

    user_role = UserRole(user_id=user_id, role_id=role_id, collection_id=collection_id)
    db.session.add(user_role)
    db.session.commit()
    return user_role


def remove_user_role(user_id, role_id, collection_id):
    user_role = UserRole.query.filter(
        UserRole.user_id == user_id,
        UserRole.collection_id == collection_id,
        UserRole.role_id == role_id).one_or_none()
    if user_role:
        db.session.delete(user_role)
        db.session.commit()


def get_users_with_role(role_name, collection):
    role = Role.get_name(role_name, required=True)

    users = User.query.join(UserRole).filter(UserRole.role_id == role.id, UserRole.collection_id == collection.id).all()
    return users


def get_collection_hierarchy():
    root = Collection.get_root_collection(required=True)
    return root.get_hierarchy_info()
