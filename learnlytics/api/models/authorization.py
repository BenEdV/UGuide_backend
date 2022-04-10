from flask_restplus import abort


from learnlytics.extensions import db
from learnlytics.database.api.apikey import PermissionGenAPI, APIKeyPermission
from learnlytics.database.authorization.collection import Collection


def authorize_gen_api(api_key, collection_id, permissions, do_abort=True):
    """
    Checks if the given api key has the given permissions for the collection
    :param token:
    :return: integer|string
    """
    collection = Collection.get(collection_id)
    ancestor_collection_ids = [collection_id]
    while collection.parent:
        collection = collection.parent
        ancestor_collection_ids.append(collection.id)

    for permission_name in permissions:
        permission = PermissionGenAPI.query.filter(PermissionGenAPI.name == permission_name).one_or_none()
        if not permission:
            if do_abort:
                abort(404, message=f"No permission with name: {permission_name} found.")
            return False

        if not APIKeyPermission.query.filter(
                APIKeyPermission.api_key_id == api_key.id,
                APIKeyPermission.permission_id == permission.id,
                APIKeyPermission.collection_id.in_(ancestor_collection_ids)).one_or_none():
            if do_abort:
                abort(401, message=f"The given api key does not have permission {permission_name} for collection")
            return False

    return True


def add_api_key_permission(api_key_id, permission_name, collection_id):
    permission = PermissionGenAPI.query.filter(PermissionGenAPI.name == permission_name).one()
    key_permission = APIKeyPermission(
        api_key_id=api_key_id,
        permission_id=permission.id,
        collection_id=collection_id)
    db.session.add(key_permission)


def add_permissions(names):
    """
    Add PermissionType object to the SQLAlchemyModel
    :param name: name of the permission
    """
    permissions = []
    for name in names:
        permissions.append(PermissionGenAPI(name=name))
    db.session.add_all(permissions)


def add_permission(name):
    """
    Add PermissionType object to the SQLAlchemyModel
    :param name: name of the permission
    """
    permission = PermissionGenAPI(name=name)
    PermissionGenAPI.add(permission)
