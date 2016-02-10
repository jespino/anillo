from anillo.adapters.werkzeug import WerkzeugAdapter


def application(handler, adapter_cls=WerkzeugAdapter):
    """Converts an anillo function based handler in a
    wsgi compiliant application function.

    :param adapter_cls: the wsgi adapter implementation (default: wekrzeug)
    :returns: wsgi function
    :rtype: callable
    """
    adapter = adapter_cls()

    def wrapper(environ, start_response):
        request = adapter.to_request(environ)
        response = handler(request)
        response_func = adapter.from_response(response)
        return response_func(environ, start_response)

    return wrapper


__all__ = ["application"]
