import functools

DEFAULT_HEADERS = frozenset(["origin", "x-requested-with", "content-type", "accept"])


def wrap_cors(func=None, *, allow_origin='*', allow_headers=DEFAULT_HEADERS):
    """
    A middleware that allow CORS calls, by adding the
    headers Access-Control-Allow-Origin and Access-Control-Allow-Headers.
    This middlware accepts two optional parameters `allow_origin` and
    `allow_headers` for customization of the headers values. By default
    will be `*` and a set of `[Origin, X-Requested-With, Content-Type, Accept]`
    respectively.
    """

    if func is None:
        return functools.partial(wrap_cors,
                                 allow_origin=allow_origin,
                                 allow_headers=allow_headers)

    _allow_headers = ", ".join(allow_headers)

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)

        if not response.headers:
            response.headers = {}

        response.headers['Access-Control-Allow-Origin'] = allow_origin
        response.headers['Access-Control-Allow-Headers'] = _allow_headers
        return response

    return wrapper
