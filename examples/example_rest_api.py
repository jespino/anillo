from anillo.app import application
from anillo.handlers.routing import router, url, context
from anillo.utils import chain
from anillo.middlewares.json import json_middleware
from anillo.http import NotFound, NoContent, Created, Ok

from werkzeug.routing import Map, Rule

database = []


def list(request):
    return Ok(database, mimetype="application/json")


def detail(request, index):
    if len(database) > index:
        return Ok(database[index], mimetype="application/json")
    else:
        return NotFound()


def create(request):
    database.append(request.data)
    return Created(request.data, mimetype="application/json")


def delete(request, index):
    if len(database) > index:
        del database[index]
        return NoContent()
    else:
        return NotFound()

urls = [
    context("/api", [
        url("/", list, methods=["get"]),
        url("/", create, methods=["post"]),
        url("/<int:index>", detail, methods=["get"]),
        url("/<int:index>", delete, methods=["delete"]),
    ])
]

app = application(chain(json_middleware, router(urls)))

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
