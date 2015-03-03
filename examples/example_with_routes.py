from anillo.app import application
from anillo.handlers.routing import router, url
from anillo.http import Ok

def index(request):
    return Ok("Index")


def hello(request):
    return Ok("Hello World!")

urls = [
    url("/", index),
    url("/hello", hello),
]

app = application(router(urls))

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
