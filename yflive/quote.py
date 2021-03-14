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
        
    
