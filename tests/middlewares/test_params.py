# -*- coding: utf-8 -*-
"""
    tests.middlwares.test_params
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests params middlewares

    :copyright: (c) 2015 by Jesús Espino.
    :license: BSD, see LICENSE for more details.
"""

from anillo.middlewares.params import form_params_middleware, get_params_middleware
from anillo.http.request import Request
from anillo.http.response import Response


@get_params_middleware
def get_app(request):
    return Response()


@form_params_middleware
def form_app(request):
    return Response()


def test_parse_get_params():
    request = Request(query_string=b"test1=test1-value&test2=test2-value&test2=test2-value2&test3=")
    get_app(request)
    assert "test1" in request.get_params
    assert request.get_params["test1"] == "test1-value"
    assert "test2" in request.get_params
    assert request.get_params["test2"] == ["test2-value", "test2-value2"]
    assert "test3" not in request.get_params


def test_parse_form_params():
    request = Request(body=b"test1=test1-value&test2=test2-value&test2=test2-value2&test3=", headers={"Content-Type": "application/x-www-form-urlencoded"})
    form_app(request)
    assert "test1" in request.form_params
    assert request.form_params["test1"] == "test1-value"
    assert "test2" in request.form_params
    assert request.form_params["test2"] == ["test2-value", "test2-value2"]
    assert "test3" not in request.form_params
