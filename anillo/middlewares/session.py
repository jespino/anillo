import uuid

def session_middleware(storage):
    def middleware(func):
        def wrapper(request):
            session_id = request.cookies.get('session-id', uuid.uuid4().hex)
            request.session = storage.retrieve(session_id)
            response = func(request)
            storage.store(session_id, request.session)
            response.set_cookie('session-id', session_id)
            return response
        return wrapper
    return middleware


class MemoryStorage:
    data = {}

    def store(self, uuid, data):
        self.data[uuid] = data

    def retrieve(self, uuid):
        return self.data.get(uuid, {})
