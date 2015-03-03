from werkzeug.wrappers import Request


def application(handler):
    def wrapper(environ, start_response):
        request = Request(environ)
        response = handler(request)
        return response(environ, start_response)
    return wrapper

__all__ = ["app_builder"]
