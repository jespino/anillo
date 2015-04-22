from cgi import parse_header
from multipart import MultipartParser
from io import BytesIO


def multipart_params_middleware(func):
    def wrapper(request):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "multipart/form-data":
            if isinstance(pdict['boundary'], str):
                pdict['boundary'] = pdict['boundary'].encode()
            mp = MultipartParser(BytesIO(request.body), pdict['boundary'])
            request.multipart_params = {}
            for part in mp:
                request.multipart_params[part.name] = {
                    "filename": part.filename,
                    "file": part.file,
                }
        return func(request)
    return wrapper
