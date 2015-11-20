import uuid
import functools


class MemoryStorage:
    def __init__(self, cookie_name="session-id"):
        self.cookie_name = cookie_name
        self.data = {}

    def get_session_key(self, request):
        session_key = request.cookies.get(self.cookie_name, {}).get('value', None)
        if session_key is None:
            return uuid.uuid4().hex
        return session_key

    def persist_session_key(self, request, response, session_key):
        if request.cookies.get(self.cookie_name, {}).get('value', None) is None:
            if hasattr(response, 'cookies'):
                response.cookies[self.cookie_name] = {"value": session_key}
            else:
                response.cookies = {self.cookie_name: {"value": session_key}}

    def store(self, request, response, session_key, data):
        self.data[session_key] = data

    def retrieve(self, request, session_key):
        return self.data.get(session_key, {})


def wrap_session(func=None, *, storage=MemoryStorage):
    """
    A middleware that adds the session management to the
    request.

    This middleware optionally accepts a `storage` keyword
    only parameter for provide own session storage
    implementation. If it is not provided, the in memory
    session storage will be used.

    :param storage: A storage factory/constructor.
    :type storage: callable or class
    """

    if func is None:
        return functools.partial(wrap_session, storage=storage)

    # Initialize the storage
    storage = storage()

    def wrapper(request, *args, **kwargs):
        session_key = storage.get_session_key(request)
        request.session = storage.retrieve(request, session_key)
        response = func(request, *args, **kwargs)

        storage.store(request, response, session_key, request.session)
        storage.persist_session_key(request, response, session_key)
        return response

    return wrapper
