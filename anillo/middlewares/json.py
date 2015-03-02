import json

def json_middleware(func):
    def wrapper(request):
        if request.mimetype == "application/json":
            request.data = json.loads(request.data.decode("utf-8"))
        response = func(request)
        if response.mimetype == "application/json":
            response.data = json.dumps(response.response)
        return response
    return wrapper
