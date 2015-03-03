from werkzeug import serving


def run_simple(app, *, host="127.0.0.1", port=500,
               debug=True, autoreload=True, **kwargs):
    """Start a WSGI application.
    Optional features include a reloader, multithreading and fork support.
    """
    kwargs.setdefault("use_evalex", debug)
    return serving.run_simple(host, port, app,
                              use_debugger=debug,
                              use_reloader=autoreload,
                              **kwargs)
