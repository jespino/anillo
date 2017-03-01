# Anillo nanoframework

[![Build Status](http://img.shields.io/travis/jespino/anillo.svg?branch=master)](https://travis-ci.org/jespino/anillo)
[![Coveralls Status](http://img.shields.io/coveralls/jespino/anillo/master.svg)](https://coveralls.io/r/jespino/anillo)
[![Development Status](https://img.shields.io/pypi/status/anillo.svg)](https://pypi.python.org/pypi/anillo/)
[![Latest Version](https://img.shields.io/pypi/v/anillo.svg)](https://pypi.python.org/pypi/anillo/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/anillo.svg)](https://pypi.python.org/pypi/anillo/)
[![License](https://img.shields.io/pypi/l/anillo.svg)](https://pypi.python.org/pypi/anillo/)

Anillo is a Ring/Compojure inspired nanoframework build on top of werkzeug
library using some utilities and the routing system.

The idea is create a really slim abstraction layer between WSGI and my
handlers, with the less quantity of opinion about what are you implementing.

You can use any template system, storage system or whatever you want, you only
receive a Request (a dict object) and must return a Response (another dict
object).

## Middlewares

You can build middlewares writing decorators, and decorating your handlers or
the router handler, if you want to affect everything.

## Routes handling

Anillo comes with a route handler based on Werkzeug Router.

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
    url("/hello", hello, methods=["get"]),
]

app = application(router(urls))

if __name__ == '__main__':
    from anillo import serving
    serving.run_simple(app, port=5000)
```
