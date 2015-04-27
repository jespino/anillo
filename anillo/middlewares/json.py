import json
from cgi import parse_header


def json_middleware(func):
    def wrapper(request):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "application/json":
            request.body = json.loads(request.body.decode("utf-8")) if request.body else None
        response = func(request)
        ctype, pdict = parse_header(response.headers.get('Content-Type', ''))
        if ctype == "application/json":
            response.body = json.dumps(response.body) if response.body else '{}'
        return response
    return wrapper
