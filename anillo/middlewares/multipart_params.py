from cgi import parse_header
from io import BytesIO

from anillo.utils.common import merge_dicts
from anillo.utils.multipart import MultipartParser


def wrap_multipart_params(func):
    """
    A middleware that parses the multipart request body and adds the
    parsed content to the `multipart_params` attribute.

    This middleware also merges the parsed value with the existing
    `params` attribute in same way as `wrap_form_params` is doing.
    """

    def wrapper(request, *args, **kwargs):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "multipart/form-data":

            if isinstance(pdict['boundary'], str):
                pdict['boundary'] = pdict['boundary'].encode()

            params = {}
            mp = MultipartParser(BytesIO(request.body), pdict['boundary'])
            for part in mp:
                params[part.name] = {
                    "filename": part.filename,
                    "file": part.file,
                }

            request.params = merge_dicts(getattr(request, "params", None), params)
            request.multipart_params = params

        return func(request, *args, **kwargs)
    return wrapper
