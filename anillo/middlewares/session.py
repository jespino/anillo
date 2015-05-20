import uuid

def session_middleware(storage):
    def middleware(func):
        def wrapper(request):
            session_key = storage.get_session_key(request)

            request.session = storage.retrieve(request, session_key)

            response = func(request)

            storage.store(request, response, session_key, request.session)

            storage.persist_session_key(request, response, session_key)

            return response
        return wrapper
    return middleware


class MemoryStorage:
    data = {}

    def __init__(self, cookie_name="session-id"):
        self.cookie_name = cookie_name

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
