import json
from urllib.parse import parse_qs
from cgi import parse_multipart, parse_header
from io import BytesIO


def multipart_params_middleware(func):
    def wrapper(request):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "multipart/form-data":
            if isinstance(pdict['boundary'], str):
                pdict['boundary'] = pdict['boundary'].encode()
            post_data = parse_multipart(BytesIO(request.body), pdict)
            request.multipart_params = {}
            for key, value in post_data.items():
                if len(value) == 1:
                    request.multipart_params[key] = value[0]
                else:
                    request.multipart_params[key] = value
        return func(request)
    return wrapper
