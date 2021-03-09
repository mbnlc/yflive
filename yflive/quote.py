import typing

import uuid

from yflive.asset_class import AssetClass
from yflive.market_state import MarketState

class Quote:
    """"""

    __fields__ = {
        "identifier": str,
        "price": float,
        "currency": str,
        "asset_class": AssetClass,
        "market_state": MarketState
    }

    def __init__(self, **kwargs):
        """"""
        self._uuid = str(uuid.uuid4())

        for (field, vtype) in self.__fields__.items():
            value = kwargs.get(field, None)
            if value is not None and vtype is not None:
                value = vtype(value)
            self.__dict__[field] = value

    def __str__(self): 
        return "{0} {1} - Price: {2} {3}, {4}".format(
                    self.asset_class, self.identifier, self.price, 
                    self.currency, self.market_state
                )
        

        

        
    
