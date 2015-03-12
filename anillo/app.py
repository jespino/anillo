from anillo.adapters.werkzeug import WerkzeugAdapter


def application(handler, adapter=WerkzeugAdapter()):
    def wrapper(environ, start_response):
        request = adapter.to_request(environ)
        response = handler(request)
        response_func = adapter.from_response(response)
        return response_func(environ, start_response)
    return wrapper


__all__ = ["application"]
