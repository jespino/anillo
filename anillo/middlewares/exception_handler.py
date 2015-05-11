def exception_handler_middleware(render_function=None, content_type="text/html"):
    if render_function is None:
        render_function = lambda tb: tb.render_full()

    def middleware(func):
        def wrapper(request):
            try:
                response = func(request)
            except Exception as e:
                tb = get_current_traceback()
                return responses.InternalServerError(render_function(tb), headers={"Content-type": content_type})

            return response
        return wrapper
    return middleware
