from anillo.app import application
from anillo.utils.common import chain
from anillo.http import Ok


def middleware(func):
    def wrapper(request):
        request.new_data = "Middleware data"
        return func(request)
    return wrapper


def index(request):
    return Ok(request.new_data)


app = application(chain(middleware, index))


if __name__ == '__main__':
    from anillo import serving
    serving.run_simple(app, port=5000)
