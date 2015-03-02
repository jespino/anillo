from anillo import anillo, router, chain
from anillo.middlewares.json import json_middleware

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response
from werkzeug.serving import run_simple

database = []


def list(request):
    return Response(database, mimetype="application/json")


def detail(request, index):
    if len(database) > index:
        return Response(database[index], mimetype="application/json")
    else:
        return Response(status=404)


def create(request):
    database.append(request.data)
    return Response(request.data, mimetype="application/json", status=201)


def delete(request, index):
    if len(database) > index:
        del database[index]
        return Response(status=204)
    else:
        return Response(status=404)

urls = Map([
    Rule("/", endpoint=list, methods=["GET"]),
    Rule("/", endpoint=create, methods=["POST"]),
    Rule("/<int:index>", endpoint=detail, methods=["GET"]),
    Rule("/<int:index>", endpoint=delete, methods=["DELETE"]),
])

app = anillo(chain(json_middleware, router(urls)))

if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
