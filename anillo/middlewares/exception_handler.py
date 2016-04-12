from anillo.http import responses
from werkzeug.debug.tbtools import get_current_traceback


def wrap_exception_handler(render_function=None, content_type="text/html"):
    if render_function is None:
        render_function = lambda tb: tb.render_full()

    def middleware(func):
        def wrapper(request, *args, **kwargs):
            try:
                response = func(request, *args, **kwargs)
            except Exception:
                tb = get_current_traceback()
                return responses.InternalServerError(render_function(tb), headers={"Content-type": content_type})

            return response
        return wrapper
    return middleware
