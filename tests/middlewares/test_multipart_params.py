# -*- coding: utf-8 -*-
"""
    tests.middlwares.test_params
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests params middlewares

    :copyright: (c) 2015 by Jesús Espino.
    :license: BSD, see LICENSE for more details.
"""

from anillo.middlewares.multipart_params import wrap_multipart_params
from anillo.http.request import Request
from anillo.http.responses import Response


@wrap_multipart_params
def multipart_app(request):
    return Response()


def test_parse_multipart_params():
    file_test_1 = ""
    file_test_2 = ""
    request = Request(
        body=b"""
----test
Content-Disposition: form-data; name=test1

test-value1
----test
Content-Disposition: form-data; name=test2; filename=test-filename

test-value2
----test--

""",
        headers={"Content-Type": "multipart/form-data; boundary=--test"}
    )
    multipart_app(request)
    assert "test1" in request.multipart_params
    assert "test1" in request.params
    assert request.multipart_params["test1"]['filename'] == None
    assert request.multipart_params["test1"]['file'].read() == b"test-value1"
    assert "test2" in request.multipart_params
    assert "test2" in request.params
    assert request.multipart_params["test2"]['filename'] == "test-filename"
    assert request.multipart_params["test2"]['file'].read() == b"test-value2"
    assert "test3" not in request.multipart_params
    assert "test3" not in request.params
