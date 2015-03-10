from anillo.http import environ_to_request, response_to_werkzeug_response


def application(handler, request_func=environ_to_request):
    def wrapper(environ, start_response):
        request = request_func(environ)
        response = handler(request)
        werkzeug_response = response_to_werkzeug_response(response)
        return werkzeug_response(environ, start_response)
    return wrapper


__all__ = ["application"]
