# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course (3 4)
# (C) Copyright Utrecht University (Department of Information and Computing Sciences)
"""
The database definition of a general api key
"""
from learnlytics.extensions import db
from learnlytics.database.basemodel import BaseModel


# Links permissions to api keys
class APIKeyPermission(db.Model):
    __tablename__ = "permissions_api_key"
    api_key_id = db.Column(
        db.Integer,
        db.ForeignKey("api_key.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    api_key = db.relationship("APIKey")

    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collection.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    collection = db.relationship("Collection")

    permission_id = db.Column(
        db.Integer,
        db.ForeignKey("permission_gen_api.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    permission = db.relationship("PermissionGenAPI")


class APIKey(BaseModel):
    """
    Allows us to add API keys to the database so that external providers can connect to our system,
    using the key we've provided to them
    """
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    key = db.Column(db.String(200))
    requester = db.Column(db.String(100))

    @classmethod
    def add_api_key(cls, key, requester):
        """
        :param key: the key to add
        :param requester: the person making the request
        """
        import bcrypt
        hashed_key = bcrypt.hashpw(str(key).encode("ascii", "ignore"), bcrypt.gensalt()).decode("ascii")
        api_key = cls(key=hashed_key, requester=requester)
        db.session.add(api_key)
        db.session.commit()
        return api_key


class PermissionGenAPI(BaseModel):
    """
    Allows us to add API keys to the database so that external providers can connect to our system,
    using the key we've provided to them
    """
    __tablename__ = "permission_gen_api"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(100))
