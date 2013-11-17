from SocketServer import BaseRequestHandler, TCPServer, ThreadingMixIn
from threading import Thread

SCHEME = "omnithinker"

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass


class RequestHandler(BaseRequestHandler):

    def _send(self, data):
        print "\x1b[32m-> \x1b[33m{0}\x1b[0m {1}".format(self._client, data)
        self.request.sendall(data + "\n")

    def _handle_chunk(self, chunk):
        print "\x1b[31m<- \x1b[33m{0}\x1b[0m {1}".format(self._client, chunk)
        self._send(chunk.upper())

    def setup(self):
        self._client = "{0}:{1}".format(self.client_address[0],
                                        self.client_address[1])
        self._send("HELLO")

    def handle(self):
        pending = ""
        while 1:
            data = self.request.recv(1024)
            if not data:
                break
            chunks = data.split("\n")
            pending += chunks.pop()
            for chunk in chunks:
                self._handle_chunk(chunk)

    def finish(self):
        self._send("BYE")


def start(host, port):
    server = ThreadedTCPServer((host, port), RequestHandler)
    print " * Running on {0}://{1}:{2}/".format(SCHEME, host, port)
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
