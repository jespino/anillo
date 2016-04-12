import json
import functools
from cgi import parse_header


def wrap_json(func=None, *, encoder=json.JSONEncoder):
    """
    A middleware that parses the body of json requests and
    encodes the json responses.

    NOTE: this middleware exists just for backward compatibility,
    but it has some limitations in terms of response body encoding
    because it only accept list or dictionary outputs and json
    specification allows store other values also.

    It is recommended use the `wrap_json_body` and wrap_json_response`
    instead of this.
    """
    if func is None:
        return functools.partial(wrap_json, encoder=encoder)

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "application/json":
            request.body = json.loads(request.body.decode("utf-8")) if request.body else None
        response = func(request, *args, **kwargs)
        if "Content-Type" in response.headers and response.headers['Content-Type'] is not None:
            ctype, pdict = parse_header(response.headers.get('Content-Type', ''))
            if ctype == "application/json" and (isinstance(response.body, dict) or isinstance(response.body, list)):
                response.body = json.dumps(response.body, cls=encoder)
        return response
    return wrapper


def wrap_json_body(func):
    """
    A middleware that parses the body of json requests and
    add it to the request under the `body` attribute (replacing
    the previous value).
    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "application/json":
            request.body = json.loads(request.body.decode("utf-8")) if request.body else None
        return func(request, *args, **kwargs)
    return wrapper


def wrap_json_params(func):
    """
    A middleware that parses the body of json requests and
    add it to the request under the `params` key.
    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "application/json":
            request.params = json.loads(request.body.decode("utf-8")) if request.body else None
        return func(request, *args, **kwargs)
    return wrapper


def wrap_json_response(func=None, *, encoder=json.JSONEncoder):
    """
    A middleware that encodes in json the response body in case
    of that the "Content-Type" header is "application/json".

    This middlware accepts and optional `encoder` parameter, that
    allow to the user specify its own json encoder class.
    """

    if func is None:
        return functools.partial(wrap_json, encoder=encoder)

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)

        if not response.body:
            return response

        ctype, pdict = parse_header(response.headers.get('Content-Type', ''))
        if ctype == "application/json":
            response.body = json.dumps(response.body, cls=encoder)
        return response

    return wrapper
