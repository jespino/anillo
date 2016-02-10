import functools

from anillo.utils.common import merge_dicts
from urllib.parse import parse_qs
from cgi import parse_header


def wrap_form_params(func):
    """
    A middleware that parses the url-encoded body and attach
    the result to the request `form_params` attribute.

    This middleware also merges the parsed value with the existing
    `params` attribute in same way as `wrap_query_params` is doing.
    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "application/x-www-form-urlencoded":
            params = {}
            for key, value in parse_qs(request.body.decode("utf-8")).items():
                if len(value) == 1:
                    params[key] = value[0]
                else:
                    params[key] = value

            request.params = merge_dicts(getattr(request, "params", None), params)
            request.form_params = params
        return func(request, *args, **kwargs)
    return wrapper


def wrap_query_params(func):
    """
    A middleware that parses the urlencoded params from the querystring
    and attach it to the request `query_params` attribute.

    This middleware also merges the parsed value with the existing
    `params` attribute in same way as `wrap_form_params` is doing.
    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        params = {}
        for key, value in parse_qs(request.query_string.decode("utf-8")).items():
            if len(value) == 1:
                params[key] = value[0]
            else:
                params[key] = value

        request.params = merge_dicts(getattr(request, "params", None), params)
        request.query_params = params
        return func(request, *args, **kwargs)
    return wrapper
