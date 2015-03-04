import json


def json_middleware(func):
    def wrapper(request):
        if request.headers.get("Content-Type", '') == "application/json":
            request.body = json.loads(request.body.decode("utf-8"))
        response = func(request)
        if response.headers.get('Content-Type', '') == "application/json":
            response.body = json.dumps(response.body)
        return response
    return wrapper
