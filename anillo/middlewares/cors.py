import functools

def wrap_cors(
    func=None,
    *,
    allow_origin='*',
    allow_headers=set(["Origin", "X-Requested-With", "Content-Type", "Accept"])):
    """
    A middleware that allow CORS calls, by adding the
    headers Access-Control-Allow-Origin and Access-Control-Allow-Headers.
    This middlware accepts two optional parameters `allow_origin` and
    `allow_headers` for customization of the headers values. By default
    will be `*` and a set of `[Origin, X-Requested-With, Content-Type, Accept]`
    respectively.
    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)

        if not response.headers:
            response.headers = {}

        response.headers['Access-Control-Allow-Origin'] = allow_origin
        response.headers['Access-Control-Allow-Headers'] = ', '.join(allow_headers)
        return response

    return wrapper
