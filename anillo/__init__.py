__version__ = (0, 0, 0)

from werkzeug.wrappers import Request, Response

def anillo(handler):
    def app(environ, start_response):
        request = Request(environ)
        response = handler(request)
        return response(environ, start_response)
    return app

def router(url_map):
    def handler(request):
        urls = url_map.bind_to_environ(request)
        endpoint, args = urls.match()
        return endpoint(request, *args)
    return handler

__all__ = ["anillo", "router"]
