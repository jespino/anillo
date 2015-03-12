class Request(dict):
    def __init__(self, server_port=None, server_name=None, remote_addr=None,
                 uri=None, query_string=None, script_name=None, scheme=None,
                 method=None, headers={}, body=None):

        super().__init__({
            "server_port": server_port,
            "server_name": server_name,
            "remote_addr": remote_addr,
            "uri": uri,
            "script_name": script_name,
            "query_string": query_string,
            "scheme": scheme,
            "method": method,
            "headers": headers,
            "body": body,
        })
        self.__dict__ = self
