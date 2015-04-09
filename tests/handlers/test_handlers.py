# -*- coding: utf-8 -*-
"""
    tests.middlwares.test_json
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests json middleware

    :copyright: (c) 2015 by Jesús Espino.
    :license: BSD, see LICENSE for more details.
"""

from anillo.handlers.routing import router, url, context
from anillo.http.request import Request
from anillo.http.response import Response


def handler1(request):
    return Response("test1")


def handler2(request, id):
    return Response("test2 - {}".format(id))


def handler3(request):
    return Response("test3")


def handler4(request, id):
    return Response("test4 - {}".format(id))


class TestRequest(Request):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server_name = "test"
        self.server_port = "80"
        self.scheme = "http"


urls = [
    url("/", handler1, methods=["get", "post"], name="handler1"),
    url("/<int:id>", handler2, methods="get", name="handler2"),
    context("/test", [
        url("/", handler3, methods=["get", "post"], name="handler3"),
        url("/<int:id>", handler4, methods=["get", "post"], name="handler4"),
    ])
]

app = router(urls)


def test_routing_root():
    request = TestRequest(uri="/", method="get")
    response = app(request)
    assert response.body == "test1"


def test_routing_root_invalid_method():
    request = TestRequest(uri="/", method="put")
    response = app(request)
    assert response.status == 405


def test_routing_by_id():
    request = TestRequest(uri="/1", method="get")
    response = app(request)
    assert response.body == "test2 - 1"


def test_routing_by_id_invalid_method():
    request = TestRequest(uri="/1", method="put")
    response = app(request)
    assert response.status == 405


def test_routing_by_id_bad_url():
    request = TestRequest(uri="/bad-id", method="get")
    response = app(request)
    assert response.status == 404


def test_routing_context_root():
    request = TestRequest(uri="/test/", method="get")
    response = app(request)
    assert response.body == "test3"


def test_routing_context_root_invalid_method():
    request = TestRequest(uri="/test/", method="put")
    response = app(request)
    assert response.status == 405


def test_routing_context_by_id():
    request = TestRequest(uri="/test/1", method="get")
    response = app(request)
    assert response.body == "test4 - 1"


def test_routing_context_by_id_invalid_method():
    request = TestRequest(uri="/test/1", method="put")
    response = app(request)
    assert response.status == 405


def test_routing_context_by_id_bad_url():
    request = TestRequest(uri="/test/bad-id", method="get")
    response = app(request)
    assert response.status == 404
