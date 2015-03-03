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
    from anillo import serving
    serving.run_simple(app, port=5000)
