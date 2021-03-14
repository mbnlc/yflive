from typing import Set, Callable

import json
import ssl

import websocket as ws

from .utils import singleton
from .reader import QuoteReader
from ._logger import _logger

# ==============================================================================
# Default callback methods
# ==============================================================================

def _on_connect(qs):
    pass

def _on_quote(qs, quote):
    _logger.info(str(quote))
    pass

def _on_error(qs, error):
    pass

def _on_close(qs):
    pass

# ==============================================================================
# QuoteStreamer singleton
# ==============================================================================

YAHOO_FINANCE_SOCKET = "wss://streamer.finance.yahoo.com/"

@singleton
class QuoteStreamer:
    """
    The QuoteStreamer streams live quote data from yahoo!finance.

    In order to receive live data we connect to the yahoo!finance websocket and
    subscribe to certain identifiers.

    The websocket responds with quotes of the financial instruments previously 
    subscribed to, which are then parced.
    """

    on_connect = _on_connect
    on_quote = _on_quote
    on_error = _on_error
    on_close = _on_close

    def __init__(self):
        self._subscribed = set()
        self._websocket = None

        self.streaming = False

    def __del__(self):
        self._websocket.close()
        if self.streaming:
            self.stop()

    def start(self):
        """
        Connect to the yahoo!finance websocket.

        Establish a connection to the yahoo!finance websocket with given
        callback methods.
        """
        try:
            self._websocket = ws.WebSocketApp(
                        YAHOO_FINANCE_SOCKET, 
                        on_error = _ws_error, 
                        on_close = _ws_close, 
                        on_message = _ws_message,
                        on_open = _ws_open)
            self._websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            self.on_error(e)
            if isinstance(e, SystemExit):
                # propagate SystemExit further
                raise
            return not isinstance(e, KeyboardInterrupt)

    def stop(self):
        """Disconnect the yahoo!finance websocket."""
        if not self.streaming: 
            _logger.warn("QuoteStreamer not streaming")
            return
        _logger.debug("Stopping QuoteStreamer...")
        self._websocket.close()
        self._websocket = None
        self.streaming = False

    @property
    def subscribed(self):
        """Get all currently tracked identifiers."""
        return self._subscribed

    def subscribe(self, identifiers=[]):
        """"""
        identifiers = set(identifiers) - self.subscribed
        self._subscribed = self.subscribed | identifiers
        if len(identifiers) <= 0: 
            return
        _logger.debug(f"Subscribing to {list(identifiers)}")
        if self.streaming:
            msg = json.dumps({"subscribe": list(identifiers)})
            self._websocket.send(msg)
        return

    def unsubscribe(self, identifiers=[]):
        """"""
        identifiers = self.subscribed & set(identifiers)
        self._subscribed = self.subscribed - identifiers
        if len(identifiers) <= 0: 
            return
        _logger.debug(f"Unsubscribing from {list(identifiers)}")
        if self.streaming and len(identifiers) > 0:
            msg = json.dumps({"subscribe": list(identifiers)})
            self._websocket.send(msg)
        return

# ==============================================================================
# Websocket callback methods
# ==============================================================================

qs = QuoteStreamer()

def _ws_open(ws):
    _logger.debug("Yahoo! Finance connection opened")
    qs.streaming = True
    qs.on_connect()
    if len(qs.subscribed) > 0:
        msg = json.dumps({"subscribe": list(qs.subscribed)})
        ws.send(msg)

def _ws_message(ws, message):
    quote = QuoteReader.parse(message)
    qs.on_quote(quote)
    
def _ws_error(ws, error):
    _logger.error("Error encountered: {0}".format(error))
    qs.on_error(error)

def _ws_close(ws):
    _logger.debug("Connection closed")
    qs.on_close()
    qs.streaming = False

