from anillo.utils.common import to_unicode

from werkzeug.http import dump_cookie
from werkzeug._internal import _cookie_parse_impl


def _parse_cookie(header, charset='utf-8', errors='replace'):
    # If the value is an unicode string it's mangled through latin1.  This
    # is done because on PEP 3333 on Python 3 all headers are assumed latin1
    # which however is incorrect for cookies, which are sent in page encoding.
    # As a result we
    if isinstance(header, str):
        header = header.encode('latin1', 'replace')

    def _parse_pairs():
        for key, val in _cookie_parse_impl(header):
            key = to_unicode(key, charset, errors, allow_none_charset=True)
            val = to_unicode(val, charset, errors, allow_none_charset=True)
            yield key, {"value": val}

    return dict(_parse_pairs())


def wrap_cookies(func):
    def wrapper(request, *args, **kwargs):
        request.cookies = _parse_cookie(request.headers.get('Cookie', 'No Cookie'))
        response = func(request, *args, **kwargs)
        if hasattr(response, 'cookies'):
            cookies_strings = []
            for key, value in response.cookies.items():
                cookies_strings.append(dump_cookie(key, **value))
            response.headers['Set-Cookie'] = cookies_strings
        return response
    return wrapper
