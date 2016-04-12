from anillo.app import application
from anillo.handlers.routing import router, url, context
from anillo.utils.common import chain
from anillo.middlewares.json import wrap_json
from anillo.http import NotFound, NoContent, Created, Ok

database = []


def list(request):
    return Ok(database, mimetype="application/json")


def detail(request, index):
    if len(database) > index:
        return Ok(database[index], mimetype="application/json")
    else:
        return NotFound()


def create(request):
    database.append(request.body)
    return Created(request.body, mimetype="application/json")


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

app = application(chain(wrap_json, router(urls)))

if __name__ == '__main__':
    from anillo import serving
    serving.run_simple(app, port=5000)
