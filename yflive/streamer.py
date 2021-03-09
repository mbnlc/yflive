from typing import Set, Callable

import json
import ssl
import logging

import websocket as ws

from yflive.utils import singleton
from yflive.reader import QuoteReader

# ==============================================================================
# Default callback methods
# ==============================================================================

def _on_connect(qs):
    pass

def _on_quote(qs, quote):
    pass

def _on_error(qs, error):
    pass

def _on_close(qs):
    pass

# ==============================================================================
# QuoteStreamer singleton
# ==============================================================================

YahooFinanceSocket = "wss://streamer.finance.yahoo.com/"
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
        self.streaming = False
        self._websocket = None

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
                        YahooFinanceSocket, 
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
            logging.warn("QuoteStreamer not streaming")
            return
        logging.debug("Stopping QuoteStreamer...")
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
        logging.debug(f"QuoteStreamer subscribing to {list(identifiers)}")
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
        logging.debug(f"QuoteStreamer unsubscribing from {list(identifiers)}")
        if self.streaming and len(identifiers) > 0:
            msg = json.dumps({"subscribe": list(identifiers)})
            self._websocket.send(msg)
        return

# ==============================================================================
# Websocket callback methods
# ==============================================================================

qs = QuoteStreamer()

def _ws_open(ws):
    logging.debug("QuoteStreamer connection opened")
    qs.streaming = True
    qs.on_connect()
    if len(qs.subscribed) > 0:
        msg = json.dumps({"subscribe": list(qs.subscribed)})
        ws.send(msg)

def _ws_message(ws, message):
    quote = QuoteReader.parse(message)
    qs.on_quote(quote)
    
def _ws_error(ws, error):
    logging.error("Error encountered: {0}".format(error))
    qs.on_error(error)

def _ws_close(ws):
    logging.debug("QuoteStreamer connection closed")
    qs.on_close()
    qs.streaming = False

