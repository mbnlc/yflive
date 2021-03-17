# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from typing import Any

import uuid

from yflive.asset_class import AssetClass
from yflive.market_state import MarketState

class Quote:
    """"""

    __fields__ = {
        "identifier": str,
        "price": float,
        "exchange": str,
        "asset_class": AssetClass,
        "market_state": MarketState
    }

    def __init__(self, identifier=None, price=None, exchange=None, 
                 asset_class: AssetClass=AssetClass.UNDEFINED,
                 market_state: MarketState=MarketState.UNDEFINED):
        """"""
        self._uuid = str(uuid.uuid4())

        self.identifier = identifier
        self.price = price
        self.exchange = exchange
        self.asset_class = asset_class
        self.market_state = market_state

    def __str__(self): 
        return "{0} {1} - Price: {2}, {3} : {4}".format(
                    self.asset_class.name, self.identifier, 
                    self.price, self.exchange,
                    self.market_state.name
                )
        
    
