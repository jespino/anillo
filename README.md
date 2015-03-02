# Anillo nanoframework

Anillo is a Ring/Compojure inspired nanoframework build on top of werkzoug
Request/Response abstraction and routing system.

The idea is create a really slim abstraction layer between WSGI and my
handlers, with the less quantity of opinion about what are you implementing.

You can use any template system, storage system or whatever you want, you only
receive a werkzoug Request and must return a werkzoug Response.

## Middlewares

You can build middlewares writing decorators, and decorating your handlers or
the router handler, if you want to affect everything.

## Examples

### Basic example

```python
from anillo import anillo

from werkzeug.wrappers import Response
from werkzeug.serving import run_simple


def index(request):
    return Response("Hello World!")


app = anillo(index)


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app)
```

### Basic with middleware

```python
from anillo import anillo

from werkzeug.wrappers import Response
from werkzeug.serving import run_simple


def middleware(func):
    def wrapper(request):
        request.new_data = "Middleware data"
        return func(request)
    return wrapper


def index(request):
    return Response(request.new_data)


app = anillo(middleware(index))


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
```

### Basic with routing

```python
from anillo import anillo, router

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

app = anillo(router(urls))

if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
```
