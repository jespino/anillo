from anillo.app import application
from anillo.utils import chain
from anillo.middlewares.session import session_middleware, MemoryStorage
from anillo.middlewares.json import json_middleware

from werkzeug.wrappers import Response
from werkzeug.serving import run_simple


def index(request):
    value = request.session.get('value', 1)
    request.session['value'] = value + 1
    return Response(request.session, mimetype="application/json")


app = application(chain(
    json_middleware,
    session_middleware(MemoryStorage()),
    index,
))


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app)
