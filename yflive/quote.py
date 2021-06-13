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
import pprint

from yflive.enums import MarketState, OptionType, QuoteType

class Quote:
    """
    The Quote object is provided for handling market data in a structured way.

    Quote instances are emitted in real-time as they are received from 
    Yahoo! Finance and offer a common interface for acquiring the data 
    provided.

    Object structure adapted from alpaca-trade-api-python Entity object.
    """

    # DO NOT CHANGE ORDER
    __fields__ = ["identifier", "price", "time", "currency", "exchange", 
                  "quoteType", "marketState", "changePercent", "dayVolume", 
                  "dayHigh", "dayLow", "change", "shortName", 
                  "expireDate", "openPrice", "previousClose", "strikePrice", 
                  "underlyingSymbol", "openInterest", "optionType", 
                  "miniOption", "lastSize", "bid", "bidSize", "ask", "askSize", 
                  "priceHint", "vol_24hr", "volAllCurrencies", "fromCurrency", 
                  "lastMarket", "circulatingSupply", "marketCap"]

    def __init__(self, **kwargs):
        """
        Initialize new Quote object.

        Provides property access to the dictionary object, based on the original
        object stored in _raw.
        """
        self._uuid = str(uuid.uuid4())
        self._raw = kwargs

    def __getattr__(self, key) -> Any:
        if key not in self.__fields__:
            raise ValueError

        if key in self._raw:
            val = self._raw[key]
            if isinstance(val, int):
                if key == "quoteType":
                    return QuoteType(val)
                elif key == "marketState":
                    return MarketState(val)
                elif key == "optionType":
                    return OptionType(val)
            else:
                return val

        return None

    def __repr__(self):
        return '{name}({raw})'.format(
            name=self.__class__.__name__,
            raw=pprint.pformat(self._raw, indent=4),
        )
        