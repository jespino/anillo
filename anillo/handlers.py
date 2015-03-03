def router(url_map):
    def handler(request):
        urls = url_map.bind_to_environ(request)
        endpoint, args = urls.match()
        return endpoint(request, **args)
    return handler

__all__ = ["router"]
