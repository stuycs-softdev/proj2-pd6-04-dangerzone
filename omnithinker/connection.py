from logging import getLogger

from .document import Document
from .protocol import *

__all__ = ["Server"]

class Connection(object):
    """Handles an open connection between the server and the JS client."""

    def __init__(self, socket):
        self._socket = socket
        self._client = id(self._socket)
        self._state = STATE_WAITING
        self._document = None

        self._logger = getLogger("gunicorn.error")
        self._log("INFO", "Connection opened.")

    def _log(self, event, data):
        """Send a debug message to the terminal."""
        events = {
            "INFO": "\x1b[33m{0} \x1b[36m!!\x1b[0m {1}",
            "SEND": "\x1b[33m{0} \x1b[31m<-\x1b[0m {1}",
            "RECV": "\x1b[33m{0} \x1b[32m->\x1b[0m {1}"
        }
        self._logger.info(events[event].format(self._client, data))

    def _send(self, verb, payload=None):
        """Send data to the client."""
        data = (verb + " " + payload) if payload else verb
        self._log("SEND", data)
        self._socket.send(data)

    def _handle_state_waiting(self, verb, data):
        """Handle input from the client when in the "waiting" state."""
        if verb == CVERB_OPEN:
            self._state = STATE_READY
            self._document = Document()
            self._send(SVERB_READY)
        else:
            self._state = STATE_CLOSING
            self._send(SVERB_INVALID, REPLY_INVALID)

    def _handle_state_ready(self, verb, data):
        """Handle input from the client when in the "ready" state."""
        if verb == CVERB_UPDATE:
            ### process update ###
            self._send(SVERB_OK)
        elif verb == CVERB_CLOSE:
            self._state = STATE_CLOSING
            self._send(SVERB_BYE)
        else:
            self._state = STATE_CLOSING
            self._send(SVERB_INVALID, REPLY_INVALID)

    def _handle_state_closing(self, verb, data):
        """Handle input from the client when in the "closing" state."""
        # Dumb client talking while we're closing the connection?
        self._send(SVERB_INVALID, REPLY_CLOSING)

    def handle(self):
        """Handle the main server/client connection loop."""
        while self._state != STATE_CLOSING:
            data = self._socket.receive()
            if not data:
                self._state = STATE_CLOSING
                break
            data = data.strip()
            self._log("RECV", data)
            verb = data.split()[0]
            if self._state == STATE_WAITING:
                self._handle_state_waiting(verb, data)
            elif self._state == STATE_READY:
                self._handle_state_ready(verb, data)
            elif self._state == STATE_CLOSING:
                self._handle_state_closing(verb, data)

    def finish(self):
        """Close the connection and save all data."""
        if self._document:
            self._document.save()
        self._log("INFO", "Connection closed.")
