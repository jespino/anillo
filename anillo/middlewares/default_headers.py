def wrap_default_headers(in_headers, out_headers):
    def middleware(func):
        def wrapper(request, *args, **kwargs):
            for header, value in in_headers.items():
                if header not in request.headers:
                    request.headers[header] = value

            response = func(request, *args, **kwargs)

            for header, value in out_headers.items():
                if header not in response.headers:
                    response.headers[header] = value

            return response
        return wrapper
    return middleware
