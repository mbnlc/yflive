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

from typing import Any

import uuid

from yflive.asset_class import AssetClass
from yflive.market_state import MarketState

class Quote:
    """
    The Quote object is provided for handling market data in a structured way.

    Quote instances are emitted in real-time as they are received from 
    Yahoo! Finance and offer a common interface for acquiring the data 
    provided.
    """

    __fields__ = {
        "identifier": str,
        "price": float,
        "exchange": str,
        "asset_class": AssetClass,
        "market_state": MarketState
    }

    def __init__(self, identifier=None, price=None, exchange=None, 
                 asset_class: AssetClass=AssetClass.NONE,
                 market_state: MarketState=MarketState.NONE):
        """
        Parameters:
        -----------
        identifier: str
            Yahoo! Finance instrument identifier
        price: <type>
            price of instrument
        exchange: str
            exchange where quote originated
        asset_class: AssetClass
            type of instrument/value
        market_state: MarketState
            trading state of underlying exchange/market
        """
        self._uuid = str(uuid.uuid4())

        self.identifier = str(identifier).upper()
        self.price = price
        self.exchange = str(exchange).lower()
        self.asset_class = asset_class
        self.market_state = market_state

    def __str__(self): 
        return "{0} {1} - Price: {2}, {3} : {4}".format(
                    self.asset_class.name, self.identifier, 
                    self.price, self.exchange,
                    self.market_state.name
                )
        
    
