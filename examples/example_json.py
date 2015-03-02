from anillo import anillo
from anillo.middlewares.json import json_middleware

from werkzeug.wrappers import Response
from werkzeug.serving import run_simple


def index(request):
    return Response({"echo-response": request.data["echo"]}, mimetype="application/json")


app = anillo(json_middleware(index))


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
