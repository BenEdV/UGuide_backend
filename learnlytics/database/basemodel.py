"""
This module defines the base model for the database object
"""

from sqlalchemy import func

from flask_restplus import abort
from . import db


class BaseModel(db.Model):
    """
    The basic model for all database models to use as framework
    """
    __abstract__ = True

    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def get(cls, primary_key, required=False):
        """
        Function returns instance of class object with the primary key of it exists
        :param primary_key: primary key (tuple if is multi column key)
        :param required: If true the call will abort if the entry is not found in database
        :return: Instance of the class or None
        """
        entry = cls.query.get(primary_key)  # pylint: disable=no-member
        if not entry and required:
            abort(404, message=f"{cls.__name__} with id: {primary_key} not found.")
        return entry

    @classmethod
    def fake_404(cls, primary_key):
        """
        Function returns a 404 for the class. This is used to hide existing resources so that a user can't retrieve
        information about resources that the user does not have access to
        :param primary_key: primary key (tuple if is multi column key)
        :return: Instance of the class or None
        """
        abort(404, message=f"{cls.__name__} with id: {primary_key} not found.")

    @classmethod
    def add(cls, instance):
        """
        Function that adds instance of class object to the database
        :param instance: instance of the class
        """
        if isinstance(instance, cls):
            db.session.add(instance)
            db.session.commit()

    @classmethod
    def upsert(cls, instance, unique, foreign_keys=None):
        """
        Function that adds instance of class object to the database if it
        doesn't already exist. In that case it updates the existing record.
        :param instance: instance of the class
        :param unique: the unique value to check for
        :param foreign_keys: keys to not update
        """
        exists = db.session.query(cls).\
            filter(getattr(cls, unique) == instance.__getattribute__(unique)).first()

        if exists:
            atr = vars(instance).keys()
            atr.remove("_sa_instance_state")
            if foreign_keys:
                for key in foreign_keys:
                    if key in atr:
                        atr.remove(key)
            for arg in atr:
                new = getattr(instance, arg)
                setattr(exists, arg, new)
        else:
            db.session.add(instance)
        db.session.commit()

    @classmethod
    def force_upsert(cls, instance, unique):
        """
        Forces the upsert by, if needed, deleting the entry, then adding
        :param instance: the instance to add
        :param unique: the unique attribute
        """
        exists = db.session.query(cls). \
            filter(getattr(cls, unique) == instance.__getattribute__(unique)).first()
        if exists:
            db.session.delete(exists)
            db.session.flush()
        cls.add(instance)

    @classmethod
    def remove(cls, instance):
        """
        Function removes instance of class object from the database
        :param instance: instance of the class
        """
        if isinstance(instance, cls):
            # pylint: disable=no-member
            db.session.delete(instance)
            db.session.commit()

    @classmethod
    def remove_by_key(cls, primary_key):
        """
        Function removes instance of class object from the database with given key if it exists
        :param :param primary_key: primary key (tuple if is multi column key)
        """
        inst = cls.get(primary_key)
        if inst is not None:
            cls.remove(inst)
