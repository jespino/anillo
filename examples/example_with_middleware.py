from anillo import anillo, chain

from werkzeug.wrappers import Response
from werkzeug.serving import run_simple


def middleware(func):
    def wrapper(request):
        request.new_data = "Middleware data"
        return func(request)
    return wrapper


def index(request):
    return Response(request.new_data)


app = anillo(chain(middleware, index))


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
