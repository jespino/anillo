import json
from urllib.parse import parse_qs


def form_params_middleware(func):
    def wrapper(request):
        if request.headers.get("Content-Type", '') == "application/x-www-form-urlencoded":
            request.form_params = parse_qs(request.body.decode("utf-8"))
        return func(request)
    return wrapper
