import sys
import functools


def chain(*args):
    return functools.reduce(lambda f1, f2: f2(f1), reversed(args))


def wsgi_decoding_dance(s, charset='utf-8', errors='replace'):
    return s.encode('latin1').decode(charset, errors)


def to_unicode(x, charset=sys.getdefaultencoding(), errors='strict',
               allow_none_charset=False):
    if x is None:
        return None
    if not isinstance(x, bytes):
        return str(x)
    if charset is None and allow_none_charset:
        return x
    return x.decode(charset, errors)


def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        if not dictionary:
            continue
        result.update(dictionary)
    return result
