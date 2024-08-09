#!/usr/bin/env python3
import io
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data = (b"GET / HTTP/1.1\r\n"
        b"User-Agent: curl/7.64.1\r\n"
        b"Host: www.example.com\r\n"
        b"Accept-Language: en, mi\r\n\r\n")

_UNKNOWN = "UNKNOWN"


class HTTPResponse(io.BufferedIOBase):
    def __init__(self, sock: socket.socket, method=None, url=None) -> None:
        super().__init__()
        self.fp = sock.makefile("rb")
        self.headers = self.msg = None

        # from the Status-Line of the response
        self.version = _UNKNOWN  # HTTP-Version
        self.status = _UNKNOWN   # Status-Code
        self.reason = _UNKNOWN   # Reason-Phrase

        self.chunked = _UNKNOWN         # is "chunked" being used?

    def read(self, size=-1, /) -> bytes:
        return self.fp.read(size)


class HTTPConnection:
    def __init__(self, host, port=80) -> None:
        self.host = host
        self.port = port
        self.sock = None

        self.__response = None

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port))

    def close(self):
        sock = self.sock
        if sock:
            self.sock = None
            sock.close()
        response = self.__response
        if response:
            self.__response = None
            response.close()

    def request(self):
        if not self.sock:
            self.connect()
        self.sock.sendall(data)

    def get_response(self):
        if self.sock:
            return HTTPResponse(sock=self.sock)
        else:
            raise ConnectionError("Connection not setup")


if __name__ == "__main__":
    h = HTTPConnection("127.0.0.1", 8000)
    h.request()
    r = h.get_response()
    print(r.read())

