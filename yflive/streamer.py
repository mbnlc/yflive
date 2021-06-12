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

from typing import Callable, Iterable

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
    subscribed to, which are then parsed.
    """

    def __init__(self, subscribe: Iterable=None, on_connect: Callable=None, 
                 on_quote: Callable=None, on_error: Callable=None, 
                 on_close: Callable=None):
        """"""

        self.on_connect = on_connect
        self.on_quote = on_quote
        self.on_error = on_error
        self.on_close = on_close

        self._subscribed = subscribe if subscribe is not None else set()

        self._websocket = None 
        self._ws_thread = None

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
            self._ws_thread = threading.Thread(target=self._run, daemon=True)
            self._ws_thread.start()
        else: 
            self._run()

    def stop(self):
        """
        Disconnect the Yahoo! Finance websocket.
        """
        if self.streaming: 
            _logger.debug("Stopping QuoteStreamer...")
            self._websocket.close()
        if isinstance(self._websocket, ws.WebSocketApp):
            self._websocket = None
        if self._ws_thread:
            self._ws_thread.join()

    def _run(self):
        try:
            self._websocket = ws.WebSocketApp(
                        YAHOO_FINANCE_SOCKET, 
                        on_error = self._ws_error, 
                        on_close = self._ws_close, 
                        on_message = self._ws_message,
                        on_open = self._ws_open)
            self._websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            self._callback(self.on_error, e)
            if isinstance(e, SystemExit):
                # propagate SystemExit further
                raise
            return not isinstance(e, KeyboardInterrupt)
        finally:
            self.stop()

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

    @property
    def subscribed(self) -> list:
        """Get all currently tracked identifiers."""
        return list(self._subscribed)

    @property
    def streaming(self) -> bool:
        """Get current streaming state."""
        if isinstance(self._websocket, ws.WebSocketApp):
            return self._websocket.keep_running
        return False
    
    def _callback(self, callback, *args):
        if callback and callable(callback):
            try:
                callback(self, *args)
            except Exception as e:
                _logger.error("error from callback {}: {}".format(callback, e))

    # ==========================================================================
    # Websocket callback methods
    # ==========================================================================

    def _ws_open(self, socket):
        _logger.debug("Yahoo! Finance connection opened")
        self._callback(self.on_connect)
        if len(self.subscribed) > 0:
            msg = json.dumps({"subscribe": list(self.subscribed)})
            socket.send(msg)

    def _ws_message(self, socket, message):
        quote = QuoteReader.parse(message)
        _logger.info(f"Quote received: {str(quote)}")
        self._callback(self.on_quote, (quote))
        
    def _ws_error(self, socket, error):
        _logger.error(error)
        self._callback(self.on_error, (error))

    def _ws_close(self, socket, status_code, reason):
        _logger.debug("Connection closed")
        self._callback(self.on_close)
        self.stop()