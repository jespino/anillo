# -*- coding: utf-8 -*-
"""
    tests.middlwares.test_params
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests params middlewares

    :copyright: (c) 2015 by Jesús Espino.
    :license: BSD, see LICENSE for more details.
"""

from anillo.http.request import Request
from anillo.http.responses import Response
from anillo.middlewares.params import wrap_form_params
from anillo.middlewares.params import wrap_query_params


@wrap_query_params
def get_app(request):
    return Response()


@wrap_form_params
def form_app(request):
    return Response()


def test_parse_query_params():
    request = Request(query_string=b"test1=test1-value&test2=test2-value&test2=test2-value2&test3=")
    get_app(request)
    assert "test1" in request.query_params
    assert "test1" in request.params
    assert request.query_params["test1"] == "test1-value"
    assert request.params["test1"] == "test1-value"
    assert "test2" in request.query_params
    assert "test2" in request.params
    assert request.query_params["test2"] == ["test2-value", "test2-value2"]
    assert request.params["test2"] == ["test2-value", "test2-value2"]
    assert "test3" not in request.query_params
    assert "test3" not in request.params


def test_parse_form_params():
    request = Request(body=b"test1=test1-value&test2=test2-value&test2=test2-value2&test3=", headers={"Content-Type": "application/x-www-form-urlencoded"})
    form_app(request)
    assert "test1" in request.form_params
    assert "test1" in request.params
    assert request.form_params["test1"] == "test1-value"
    assert request.params["test1"] == "test1-value"
    assert "test2" in request.form_params
    assert "test2" in request.params
    assert request.form_params["test2"] == ["test2-value", "test2-value2"]
    assert request.params["test2"] == ["test2-value", "test2-value2"]
    assert "test3" not in request.form_params
    assert "test3" not in request.params
