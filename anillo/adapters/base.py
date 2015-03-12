from abc import ABCMeta, abstractmethod


class WsgiAdapter(metaclass=ABCMeta):
    @abstractmethod
    def to_request(self, environ):
        pass

    @abstractmethod
    def from_response(self, response):
        pass
