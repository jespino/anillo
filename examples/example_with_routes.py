from anillo.app import application
from anillo.handlers import router

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response
from werkzeug.serving import run_simple


def index(request):
    return Response("Index")


def hello(request):
    return Response("Hello World!")

urls = Map([
    Rule("/", endpoint=index),
    Rule("/hello", endpoint=hello),
])

app = application(router(urls))

if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
