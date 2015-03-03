from werkzeug.wrappers import BaseRequest
from werkzeug.wrappers import AcceptMixin
from werkzeug.wrappers import ETagRequestMixin
from werkzeug.wrappers import UserAgentMixin
from werkzeug.wrappers import AuthorizationMixin
from werkzeug.wrappers import CommonRequestDescriptorsMixin
from werkzeug.wrappers import StreamOnlyMixin


class Request(BaseRequest, AcceptMixin, ETagRequestMixin,
              UserAgentMixin, AuthorizationMixin,
              CommonRequestDescriptorsMixin):
    """Full featured request object implementing the following mixins:

    - :class:`AcceptMixin` for accept header parsing
    - :class:`ETagRequestMixin` for etag and cache control handling
    - :class:`UserAgentMixin` for user agent introspection
    - :class:`AuthorizationMixin` for http auth handling
    - :class:`CommonRequestDescriptorsMixin` for common headers
    """


class PlainRequest(StreamOnlyMixin, Request):
    """A request object without special form parsing capabilities."""
