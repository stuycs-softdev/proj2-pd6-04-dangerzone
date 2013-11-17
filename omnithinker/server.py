from datetime import datetime
from SocketServer import BaseRequestHandler, TCPServer, ThreadingMixIn
from threading import Thread

from .document import Document
from .protocol import *

__all__ = ["Server"]

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Implements a TCP server that creates threads to handle connections."""
    pass


class RequestHandler(BaseRequestHandler):
    """Handles an open connection between the server and the JS client."""

    def _debug(self, event, data):
        """Send a debug message to the terminal."""
        events = {
            "INFO": "\x1b[36m!! \x1b[33m{0}\x1b[0m [{1}] {2}",
            "SEND": "\x1b[32m-> \x1b[33m{0}\x1b[0m [{1}] {2}",
            "RECV": "\x1b[31m<- \x1b[33m{0}\x1b[0m [{1}] {2}"
        }
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        print events[event].format(self._client, now, data)

    def _send(self, verb, payload=None):
        """Send data to the client."""
        data = (verb + " " + payload) if payload else verb
        self._debug("SEND", data)
        self.request.sendall(data + "\n")

    def _handle_state_waiting(self, verb, chunk):
        """Handle input from the client when in the "waiting" state."""
        if verb == CVERB_OPEN:
            self._status = STATE_READY
            self._document = Document()
            self._send(SVERB_READY)
        else:
            self._status = STATE_CLOSING
            self._send(SVERB_INVALID, REPLY_INVALID)

    def _handle_state_ready(self, verb, chunk):
        """Handle input from the client when in the "ready" state."""
        if verb == CVERB_UPDATE:
            ### process update ###
            self._send(SVERB_OK)
        elif verb == CVERB_CLOSE:
            self._status = STATE_CLOSING
            self._send(SVERB_BYE)
        else:
            self._status = STATE_CLOSING
            self._send(SVERB_INVALID, REPLY_INVALID)

    def _handle_state_closing(self, verb, chunk):
        """Handle input from the client when in the "closing" state."""
        # Dumb client talking while we're closing the connection?
        self._send(SVERB_INVALID, REPLY_CLOSING)

    def _handle_chunk(self, chunk):
        """Handle a chunk of input from the client."""
        self._debug("RECV", chunk)
        verb = chunk.split()[0]
        if self._status == STATE_WAITING:
            self._handle_state_waiting(verb, chunk)
        elif self._status == STATE_READY:
            self._handle_state_ready(verb, chunk)
        elif self._status == STATE_CLOSING:
            self._handle_state_closing(verb, chunk)

    def setup(self):
        """Set up the connection."""
        self._client = "{0}:{1}".format(self.client_address[0],
                                        self.client_address[1])
        self._status = STATE_WAITING
        self._document = None
        self._debug("INFO", "Connection opened.")

    def handle(self):
        """Handle the main server/client connection loop."""
        pending = ""
        while self._status != STATE_CLOSING:
            data = self.request.recv(1024)
            if not data:
                break
            chunks = data.split("\n")
            pending += chunks.pop()
            for chunk in chunks:
                if chunk:
                    self._handle_chunk(chunk)

    def finish(self):
        """Close the connection and save all data."""
        if self._document:
            self._document.save()
        self._debug("INFO", "Connection closed.")


class Server(object):
    """Manages the OmniThinker Python<->JS server."""
    SCHEME = "omnithinker"

    def __init__(self, host, port):
        self._host, self._port = host, port
        self._server = ThreadedTCPServer((host, port), RequestHandler)

    def start(self):
        msg_template = " * Running on {0}://{1}:{2}/"
        print msg_template.format(self.SCHEME, self._host, self._port)
        thread = Thread(target=self._server.serve_forever)
        thread.daemon = True
        thread.start()

    def stop(self):
        self._server.shutdown()
