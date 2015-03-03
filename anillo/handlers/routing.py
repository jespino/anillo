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

from werkzeug.routing import Map, Rule, Submount
from werkzeug.exceptions import NotFound, MethodNotAllowed

import anillo.http as http


def url(match, handler=None, methods=None, defaults=None,
        redirect_to=None, build_only=False, **kwargs):
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
            "build_only": build_only}

    rule.update(kwargs)
    return rule


def context(match, urls):
    """A helper that provides a way of giving a common
    prefix to a set of routes.

    :return: The anillo url spec for url nesting.
    :rtype: dict
    """
    return {"context": match
            "routes": urls}


def _build_rules(specs):
    """Adapts the list of anillo urlmapping specs into
    a list of werkzeug rules or rules subclasses.

    :param list specs: A list of anillo url mapping specs.
    :return: generator
    """
    for spec in specs:
        if "context" in spec:
            yield Submount(spec["context"], list(_build_rules(spec.get("routes", []))))
        else:
            spec = spec.copy()
            match = rulespec.pop("match")
            handler = rulespec.pop("handler")
            yield Rule(match, endpoint=handler, **spec)


def _build_urlmapping(urls):
    """Convers the anillo urlmappings list into
    werkzeug Map instance.

    :return: a werkzeug Map instance
    :rtype: Map
    """

    rules = _build_rules(urls)
    return Map(list(rules))


def default_match_error_handler(exc):
    """
    Default implementation for match error handling.
    """
    if isinstance(exc, NotFound):
        return http.NotFound()
    elif isinstance(exc, MethodNotAllowed):
        return http.MethodNotAllowed()
    else:
        raise exc


def router(specs, match_error=default_match_error_handler):
    urlmapping = _build_urlmapping(specs)

    def handler(request):
        urls = urlmapping.bind_to_environ(request)
        try:
            endpoint, args = urls.match()
        except (NotFound, MethodNotAllowed) as exc:
            return match_error(exc)
        else:
            return endpoint(request, **args)

    return handler


__all__ = ["router", "url", "context"]
