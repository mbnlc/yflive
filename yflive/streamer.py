# Copyright 2021 Max Beinlich

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

import json
import ssl
import threading
import logging

import websocket as ws

from ._reader import QuoteReader

__all__ = ['YAHOO_FINANCE_SOCKET', 'QuoteStreamer']

_logger = logging.getLogger("yflive")

# ==============================================================================
# QuoteStreamer
# ==============================================================================

YAHOO_FINANCE_SOCKET = "wss://streamer.finance.yahoo.com/"

class QuoteStreamer:
    """
    The QuoteStreamer streams live quote data from yahoo!finance.

    In order to receive live data we connect to the yahoo!finance websocket and
    subscribe to certain identifiers.

    The websocket responds with quotes of the financial instruments previously 
    subscribed to, which are then parced.
    """

    on_connect = None
    on_quote = None
    on_error = None
    on_close = None

    instance = None

    def __init__(self, enable_trace: bool=False):
        """Get QuoteStreamer singleton"""
        self._subscribed = set()
        self._websocket = None

        ws.enableTrace(enable_trace)

        self._ws_thread = None

    def __new__(cls, **kwargs):
        if not cls.instance:
            cls.instance = super(QuoteStreamer, cls).__new__(cls, **kwargs)
        return cls.instance

    def __del__(self):
        self.stop()

    def start(self, blocking=True):
        """
        Connect to the yahoo!finance websocket.

        Establish a connection to the yahoo!finance websocket with given
        callback methods.

        Parameters:
        -----------
        blocking: bool 
            True <default>
            False -> Run on non blocking Thread
        """
        if blocking is False:
            self._ws_thread = threading.Thread(target=self._run)
            self._ws_thread.daemon = True
            self._ws_thread.start()
        else: 
            self._run()


    def stop(self):
        """
        Disconnect the Yahoo! Finance websocket.
        """
        if not self.streaming: 
            return
        _logger.debug("Stopping QuoteStreamer...")
        if isinstance(self._websocket, ws.WebSocketApp):
            self._websocket.close()
            self._websocket = None
        if self._ws_thread:
            self._ws_thread.join()

    def _run(self):
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
            self.stop()
            return not isinstance(e, KeyboardInterrupt)

    @property
    def subscribed(self) -> List:
        """Get all currently tracked identifiers."""
        return list(self._subscribed)

    @property
    def streaming(self) -> bool:
        """Get current streaming state."""
        return self._websocket is not None

    def subscribe(self, identifiers=None):
        """
        Subscribe to identifiers.
        
        Parameters:
        -----------
        identifiers: <type>
            identifiers to subscribe to
        """
        if identifiers is None and len(identifiers) <= 0:
            return
        identifiers = set(identifiers) - self._subscribed
        self._subscribed = self._subscribed | identifiers
        _logger.debug(f"Subscribing to {list(identifiers)}")
        if self.streaming and len(identifiers) > 0:
            msg = json.dumps({"subscribe": list(identifiers)})
            self._websocket.send(msg)
        return

    def unsubscribe(self, identifiers=None):
        """
        Unsubscribe from identifiers.
        
        Parameters:
        -----------
        identifiers: <type>
            identifiers to unsubscribe from
        """
        if identifiers is None and len(identifiers) <= 0:
            return
        identifiers = self._subscribed & set(identifiers)
        self._subscribed = self._subscribed - identifiers
        _logger.debug(f"Unsubscribing from {list(identifiers)}")
        if self.streaming and len(identifiers) > 0:
            msg = json.dumps({"unsubscribe": list(identifiers)})
            self._websocket.send(msg)
        return

# ==============================================================================
# Websocket callback methods
# ==============================================================================

_streamer = QuoteStreamer()

def _ws_open(ws):
    _logger.debug("Yahoo! Finance connection opened")
    if _streamer.on_connect:
        _streamer.on_connect()
    if len(_streamer.subscribed) > 0:
        msg = json.dumps({"subscribe": list(_streamer.subscribed)})
        ws.send(msg)

def _ws_message(ws, message):
    quote = QuoteReader.parse(message)
    _logger.info(f"Quote received: {str(quote)}")
    if _streamer.on_quote:
        _streamer.on_quote(quote)
    
def _ws_error(ws, error):
    _logger.error(f"Error encountered: {error}")
    if _streamer.on_error:
        _streamer.on_error(error)

def _ws_close(ws):
    _logger.debug("Connection closed")
    if _streamer.on_close:
        _streamer.on_close()
    _streamer.stop()