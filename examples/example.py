from anillo import anillo

from werkzeug.wrappers import Response
from werkzeug.serving import run_simple


def index(request):
    return Response("Hello World!")


app = anillo(index)


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app)
