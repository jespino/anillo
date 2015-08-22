from anillo.utils.common import wsgi_decoding_dance
from anillo.http.request import Request
from werkzeug.wsgi import get_input_stream
from werkzeug.wrappers import BaseResponse

from .base import WsgiAdapter


class WerkzeugResponse(BaseResponse):
    pass


class AnilloAdapter(WsgiAdapter):
    def _get_wsgi_headers(self, environ):
        def _unicodify_header_value(value):
            if isinstance(value, bytes):
                value = value.decode('latin-1')
            if not isinstance(value, str):
                value = str(value)
            return value

        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_') and key not in ('HTTP_CONTENT_TYPE', 'HTTP_CONTENT_LENGTH'):
                key = key[5:].replace('_', '-').title()
                value = _unicodify_header_value(value)
                headers[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').title()
                value = _unicodify_header_value(value)
                headers[key] = value
        return headers

    def to_request(self, environ):
        uri = wsgi_decoding_dance(environ.get('PATH_INFO', ''), 'utf-8')
        uri = '/' + uri.lstrip('/')

        request = Request(
            server_port=environ.get('SERVER_PORT', None),
            server_name=environ.get('SERVER_NAME', None),
            remote_addr=environ.get('REMOTE_ADDR', None),
            uri=uri,
            script_name=wsgi_decoding_dance(environ.get('SCRIPT_NAME', ''), 'utf-8'),
            query_string=environ.get('QUERY_STRING', '').encode('latin1'),
            scheme=environ.get('wsgi.url_scheme', None),
            method=environ.get('REQUEST_METHOD', "").upper(),
            headers=self._get_wsgi_headers(environ),
            body=get_input_stream(environ).read()
        )
        return request

    def from_response(self, response):
        return WerkzeugResponse(response.body, status=response.status, headers=response.headers)
