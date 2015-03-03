from anillo.app import application
from anillo.utils import chain
from anillo.http import Ok
from anillo.middlewares.session import session_middleware, MemoryStorage
from anillo.middlewares.json import json_middleware


def index(request):
    value = request.session.get('value', 1)
    request.session['value'] = value + 1
    return Ok(request.session, mimetype="application/json")


app = application(chain(
    json_middleware,
    session_middleware(MemoryStorage()),
    index,
))


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app)
