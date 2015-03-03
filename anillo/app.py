from anillo.http import Request


def application(handler, request_cls=Request):
    def wrapper(environ, start_response):
        request = request_cls(environ)
        response = handler(request)
        return response(environ, start_response)
    return wrapper


__all__ = ["application"]
