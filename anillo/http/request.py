from werkzeug._compat import wsgi_decoding_dance
from werkzeug.wsgi import get_input_stream


def _get_wsgi_headers(environ):
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


class Request(dict):
    def __init__(self, server_port=None, server_name=None, remote_addr=None,
                 uri=None, query_string=None, script_name=None, scheme=None,
                 request_method=None, headers={}, body=None):

        super().__init__({
            "server_port": server_port,
            "server_name": server_name,
            "remote_addr": remote_addr,
            "uri": uri,
            "script_name": script_name,
            "query_string": query_string,
            "scheme": scheme,
            "request_method": request_method,
            "headers": headers,
            "body": body,
        })
        self.__dict__ = self


def environ_to_request(environ):
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
        request_method=environ.get('REQUEST_METHOD', "").upper(),
        headers=_get_wsgi_headers(environ),
        body=get_input_stream(environ).read()
    )
    return request
