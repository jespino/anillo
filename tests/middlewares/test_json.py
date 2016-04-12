# -*- coding: utf-8 -*-
"""
    tests.middlwares.test_json
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests json middleware

    :copyright: (c) 2015 by Jesús Espino.
    :license: BSD, see LICENSE for more details.
"""

from anillo.http.request import Request
from anillo.http.responses import Response
from anillo.middlewares.json import wrap_json
from anillo.middlewares.json import wrap_json_body
from anillo.middlewares.json import wrap_json_params
from anillo.middlewares.json import wrap_json_response


# TODO: test new middlewares

@wrap_json
def json_app1(request):
    response = Response(request.body["test"],
                        headers={"Content-Type": "text/plain"})
    return response


@wrap_json
def json_app2(request):
    response = Response({"test": "test value"},
                        headers={"Content-Type": "application/json"})
    return response


@wrap_json
def json_app3(request):
    response = Response(request.body,
                        headers={"Content-Type": "text/plain"})
    return response


@wrap_json
def json_app4(request):
    response = Response({"test": "test value"},
                        headers={"Content-Type": "text/plain"})
    return response

@wrap_json
def json_app5(request):
    response = Response("not-dict-or-list-value",
                        headers={"Content-Type": "text/plain"})
    return response


def test_parse_json_content():
    request = Request()
    request.body = b'{"test": "test value"}'
    request.method = "POST"
    request.headers = {"Content-Type": "application/json"}
    response = json_app1(request)
    assert response.body == "test value"


def test_parse_json_content_with_charset():
    request = Request()
    request.body = b'{"test": "test value"}'
    request.method = "POST"
    request.headers = {"Content-Type": "application/json; charset=UTF-8"}
    response = json_app1(request)
    assert response.body == "test value"


def test_return_json_content():
    request = Request()
    response = json_app2(request)
    assert response.body == '{"test": "test value"}'


def test_no_parse_json_content_with_bad_content_type():
    request = Request()
    request.body = b'{"test": "test value"}'
    request.method = "POST"
    request.headers = {"Content-Type": "text/plain"}
    response = json_app3(request)
    assert response.body == b'{"test": "test value"}'


def test_no_return_json_content_with_bad_content_type():
    request = Request()
    response = json_app4(request)
    assert response.body == {"test": "test value"}

def test_no_convert_the_json_content_not_list_or_dict_content():
    request = Request()
    response = json_app5(request)
    assert response.body == "not-dict-or-list-value"
