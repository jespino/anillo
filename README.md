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
from anillo.app import application
from anillo.http import Ok


def index(request):
    return Ok("Hello World!")


app = application(index)


if __name__ == '__main__':
    from anillo import serving
    serving.run_simple(app, port=5000)
```

### Basic with middleware

```python
from anillo.app import application
from anillo.utils import chain
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
```

### Basic with routing

```python
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
```
