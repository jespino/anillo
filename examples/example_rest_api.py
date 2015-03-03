from anillo.app import application
from anillo.handlers import router
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

urls = Map([
    Rule("/", endpoint=list, methods=["GET"]),
    Rule("/", endpoint=create, methods=["POST"]),
    Rule("/<int:index>", endpoint=detail, methods=["GET"]),
    Rule("/<int:index>", endpoint=delete, methods=["DELETE"]),
])

app = application(chain(json_middleware, router(urls)))

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
