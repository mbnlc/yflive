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
        
    
