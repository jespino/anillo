from anillo.http.request import Request
from anillo.utils.structures import CaseInsensitiveDict
from werkzeug.wsgi import get_input_stream
from werkzeug.wrappers import BaseResponse, Request as WerkzeugRequest

from .base import WsgiAdapter


class WerkzeugResponse(BaseResponse):
    pass


class WerkzeugAdapter(WsgiAdapter):
    def to_request(self, environ):
        werkzeug_request = WerkzeugRequest(environ)

        request = Request(
            server_port=environ.get('SERVER_PORT', None),
            server_name=environ.get('SERVER_NAME', None),
            remote_addr=werkzeug_request.remote_addr,
            uri=werkzeug_request.path,
            script_name=werkzeug_request.script_root,
            query_string=werkzeug_request.query_string,
            scheme=werkzeug_request.scheme,
            method=werkzeug_request.method,
            headers=CaseInsensitiveDict(dict(werkzeug_request.headers)),
            body=get_input_stream(environ).read()
        )

        return request

    def from_response(self, response):
        return WerkzeugResponse(response['body'], status=response['status'], headers=dict(response['headers']))
