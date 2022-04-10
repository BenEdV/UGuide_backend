# coding=utf-8
"""
This module contains the test for the widget interface
"""
from flask import render_template, make_response
from flask_restplus import Resource
from pychartjs import BaseChart, ChartType, Color

from create_api import widget_hello_ns as ns


@ns.route('')
class HelloWorldResource(Resource):
    """
    This class is the resource endpoint for testing the widget interface
    """

    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        return make_response(render_template("hello.html"), 200)


class TestBarGraph(BaseChart):
    type = ChartType.Bar

    class data:
        label = "Numbers"
        data = [12, 19, 3, 17, 10]
        backgroundColor = Color.Green


@ns.route('/chart')
class ChartTestResource(Resource):
    """
    This class is the resource endpoint for testing the charts library
    """

    @ns.response(200, 'Success')
    def get(self):  # pylint: disable=no-self-use
        TestChart = TestBarGraph()
        ChartJSON = TestChart.get()
        return make_response(render_template("chart_test.html", chartJSON=ChartJSON), 200)
