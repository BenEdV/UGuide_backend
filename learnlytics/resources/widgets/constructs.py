# coding=utf-8
"""
This module contains the serving widgets with data concerning the construct of a course
"""
from flask import render_template, make_response
from flask_restplus import Resource

from create_api import widget_constructs_ns as ns
from learnlytics.database.authorization.collection import Collection
from learnlytics.models.construct import Constructs


@ns.route('/')
class WidgetConstructResource(Resource):
    """
    This class is the resource endpoint for the widget for the overview of the constructs of a collection
    """

    @ns.response(200, 'Success')
    def get(self, collection_id):  # pylint: disable=no-self-use
        collection = Collection.get(collection_id, required=True)
        if collection.settings is None or not collection.settings.get("allow_widgets", False):
            return "Widgets have not been enabled for this collection", 403

        constructs = Constructs.get_collection_constructs(collection_id)

        response = make_response(
            render_template(
                "constructs_overview.html",
                collection=collection,
                constructs=constructs
            ),
            200
        )

        return response
