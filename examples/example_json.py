from anillo.app import application
from anillo.middlewares.json import json_middleware
from anillo.http import Ok


def index(request):
    return Ok({"echo-response": request.data["echo"]}, mimetype="application/json")


app = application(json_middleware(index))


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
