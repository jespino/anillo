# -*- coding: utf-8 -*-
"""
    tests.middlwares.test_cookies
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests cookies middleware

    :copyright: (c) 2015 by Jesús Espino.
    :license: BSD, see LICENSE for more details.
"""

from anillo.middlewares.cookies import wrap_cookies
from anillo.http.request import Request
from anillo.http.responses import Response


@wrap_cookies
def cookie_app(request):
    response = Response(request.cookies if request.cookies else "No Cookie",
                        headers={"Content-Type": 'text/plain'},
                        cookies={'test': {'value': 'test'}})
    return response


def test_cookie_forging():
    request = Request(headers={"Cookie": "foo=bar"})
    response = cookie_app(request)
    assert response.body == {"foo": {"value": "bar"}}


def test_set_cookie_app():
    request = Request()
    response = cookie_app(request)
    assert 'Set-Cookie' in dict(response.headers)
    assert response.headers['Set-Cookie'] == ["test=test; Path=/"]


def test_no_initial_cookie():
    request = Request()
    response = cookie_app(request)
    assert response.body == "No Cookie"
