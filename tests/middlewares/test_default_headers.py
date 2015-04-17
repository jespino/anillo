# -*- coding: utf-8 -*-
"""
    tests.middlwares.test_session
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests session middleware

    :copyright: (c) 2015 by Jesús Espino.
    :license: BSD, see LICENSE for more details.
"""

from anillo.middlewares.default_headers import default_headers_middleware
from anillo.http.request import Request
from anillo.http.responses import Response


@default_headers_middleware({"in-test": "in-test-value"}, {"out-test": "out-test-value"})
def session_app(request):
    if request.headers['in-test'] == "in-test-other-value":
        return Response(headers={"out-test": "out-test-other-value"})
    else:
        return Response()


def test_default_header_without_headers():
    request = Request()
    response = session_app(request)
    assert "in-test" in request.headers
    assert request.headers['in-test'] == "in-test-value"
    assert "out-test" in response.headers
    assert response.headers['out-test'] == "out-test-value"


def test_default_header_with_headers():
    request = Request(headers={"in-test": "in-test-other-value"})
    response = session_app(request)
    assert "in-test" in request.headers
    assert request.headers['in-test'] == "in-test-other-value"
    assert "out-test" in response.headers
    assert response.headers['out-test'] == "out-test-other-value"
