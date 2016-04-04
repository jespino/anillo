"""
Url routing module.

This module provides to anillo nanoframework a handler that manages the
url matching and routing. It is hightly inspired by clojure's compojure
library and other similar ones.

This is a little example on how you can define routes:

  urls = [
      url("/<int:year>", index, methods=["get", "post"]),
      url("/<int:year>", index, methods=["get", "post"])

      context("/blog", [
          url("/<int:year>", index, methods=["get", "post"]),
          url("/<int:year>", index, methods=["get", "post"])
      ])
  ]
"""

from werkzeug.routing import Map as WerkzeugMap, Rule as WerkzeugRule, RuleFactory, RequestRedirect
from werkzeug.exceptions import NotFound, MethodNotAllowed
from werkzeug.utils import redirect

import anillo.http as http


class Rule(WerkzeugRule):
    def __init__(self, *args, **kwargs):
        self.handler = kwargs.pop('handler', None)
        self.extra_data = kwargs.pop('extra_data', {})
        super().__init__(*args, **kwargs)


class Context(RuleFactory):
    def __init__(self, path, rules):
        self.path = path.rstrip('/')
        self.rules = rules

    def get_rules(self, map):
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                rule.rule = self.path + rule.rule
                yield rule


class Map(WerkzeugMap):
    def bind_to_request(self, request, server_name=None, subdomain=None):
        if server_name is None:
            if 'HTTP_HOST' in request.headers:
                server_name = request.headers['HTTP_HOST']
            else:
                server_name = request.server_name
                if (request.scheme, request.server_port) not in (('https', '443'), ('http', '80')):
                    server_name += ':' + request.server_port
        elif subdomain is None:
            server_name = server_name.lower()
            if 'HTTP_HOST' in request.headers:
                wsgi_server_name = request.headers.get('HTTP_HOST')
            else:
                wsgi_server_name = request.server_name
                if (request.scheme, request.server_port) not in (('https', '443'), ('http', '80')):
                    wsgi_server_name += ':' + request.server_port
            wsgi_server_name = wsgi_server_name.lower()
            cur_server_name = wsgi_server_name.split('.')
            real_server_name = server_name.split('.')
            offset = -len(real_server_name)
            if cur_server_name[offset:] != real_server_name:
                # This can happen even with valid configs if the server was
                # accesssed directly by IP address under some situations.
                # Instead of raising an exception like in Werkzeug 0.7 or
                # earlier we go by an invalid subdomain which will result
                # in a 404 error on matching.
                subdomain = '<invalid>'
            else:
                subdomain = '.'.join(filter(None, cur_server_name[:offset]))

        path_info = request.uri
        return Map.bind(self, server_name, request.script_name,
                        subdomain, request.scheme,
                        request.method, path_info,
                        query_args=request.query_string)


def optionize(url):
    real_handler = url['handler']

    def handler(request, *args, **kwargs):
        if request.method == "OPTIONS":
            return http.Ok("", headers={
                "Access-Control-Allow-Methods": ",".join(url['methods'])
            })
        return real_handler(request, *args, **kwargs)

    url['handler'] = handler
    url['methods'].append("OPTIONS")
    return url


def url(match, handler=None, methods=None, defaults=None,
        redirect_to=None, build_only=False, name=None, **kwargs):
    """Simple helper for build a url, and return anillo
    url spec hash map (dictionary)

    It can be used in this way:

    urls = [
        url("/<int:year>", index, methods=["get", "post"]),
        url("/<int:year>", index, methods=["get", "post"])
    ]

    This is a prefered way to define one url.

    :return: The anillo url spec
    :rtype: dict
    """
    assert isinstance(match, str), "match parameter should be string."
    assert handler or redirect_to, "you should specify handler or redirect_to for the url"

    if isinstance(methods, str):
        methods = [methods.upper()]
    elif isinstance(methods, (list, tuple)):
        methods = [x.upper() for x in methods]

    rule = {"match": match,
            "handler": handler,
            "methods": methods,
            "defaults": defaults,
            "redirect_to": redirect_to,
            "build_only": build_only,
            "name": name,
            "extra_data": kwargs}
    return rule


def optionized_url(*args, **kwargs):
    return optionize(url(*args, **kwargs))


def reverse(specs, name, **kwargs):
    absolute_url = kwargs.pop('absolute_url', '')
    urlmapping = _build_urlmapping(specs)
    urls = urlmapping.bind(absolute_url)
    return urls.build(name, kwargs)


def context(match, urls):
    """A helper that provides a way of giving a common
    prefix to a set of routes.

    :return: The anillo url spec for url nesting.
    :rtype: dict
    """
    return {"context": match,
            "routes": urls}


def _build_rules(specs):
    """Adapts the list of anillo urlmapping specs into
    a list of werkzeug rules or rules subclasses.

    :param list specs: A list of anillo url mapping specs.
    :return: generator
    """
    for spec in specs:
        if "context" in spec:
            yield Context(spec["context"], list(_build_rules(spec.get("routes", []))))
        else:
            rulespec = spec.copy()
            match = rulespec.pop("match")
            name = rulespec.pop("name")
            yield Rule(match, endpoint=name, **rulespec)


def _build_urlmapping(urls, strict_slashes=False, **kwargs):
    """Convers the anillo urlmappings list into
    werkzeug Map instance.

    :return: a werkzeug Map instance
    :rtype: Map
    """

    rules = _build_rules(urls)
    return Map(rules=list(rules), strict_slashes=strict_slashes, **kwargs)


def default_match_error_handler(exc):
    """
    Default implementation for match error handling.
    """
    if isinstance(exc, NotFound):
        return http.NotFound()
    elif isinstance(exc, MethodNotAllowed):
        return http.MethodNotAllowed()
    elif isinstance(exc, RequestRedirect):
        return redirect(exc.new_url)
    else:
        raise exc


def router(specs, match_error=default_match_error_handler, **kwargs):
    urlmapping = _build_urlmapping(specs, **kwargs)

    def handler(request):
        urls = urlmapping.bind_to_request(request)
        try:
            rule, args = urls.match(return_rule=True)
        except Exception as exc:
            return match_error(exc)
        else:
            request.router_rule = rule
            return rule.handler(request, **args)

    return handler


__all__ = ["router", "url", "context"]
