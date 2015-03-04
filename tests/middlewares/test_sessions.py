# -*- coding: utf-8 -*-
"""
    tests.middlwares.test_session
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests session middleware

    :copyright: (c) 2015 by Jesús Espino.
    :license: BSD, see LICENSE for more details.
"""

from anillo.middlewares.cookies import cookies_middleware
from anillo.middlewares.session import session_middleware, MemoryStorage
from anillo.http.request import Request
from anillo.http.response import Response


@cookies_middleware
@session_middleware(MemoryStorage())
def session_app(request):
    request.session["test"] = request.session.get("test", 0) + 1
    response = Response(request.session["test"])
    return response


def test_session_without_cookie():
    request = Request()
    response = session_app(request)
    assert response.body == 1
    response = session_app(request)
    assert response.body == 1


def test_session_with_cookie():
    request = Request()
    response = session_app(request)
    assert response.body == 1

    session_id = response.cookies['session-id']['value']

    request = Request(headers={"Cookie": "session-id={}".format(session_id)})
    response = session_app(request)
    assert response.body == 2
