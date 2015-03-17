import json
from urllib.parse import parse_qs


def form_params_middleware(func):
    def wrapper(request):
        if request.headers.get("Content-Type", '') == "application/x-www-form-urlencoded":
            request.form_params = {}
            for key, value in parse_qs(request.body.decode("utf-8")).items():
                if len(value) == 1:
                    request.form_params[key] = value[0]
                else:
                    request.form_params[key] = value
        return func(request)
    return wrapper

def get_params_middleware(func):
    def wrapper(request):
        request.get_params = {}
        for key, value in parse_qs(request.query_string.decode("utf-8")).items():
            if len(value) == 1:
                request.get_params[key] = value[0]
            else:
                request.get_params[key] = value
        return func(request)
    return wrapper
