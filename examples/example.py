from anillo.app import application
from anillo.http import Ok


def index(request):
    return Ok("Hello World!")


app = application(index)


if __name__ == '__main__':
    from anillo import serving
    serving.run_simple(app, port=5000)
