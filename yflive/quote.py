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

import typing

import uuid

from yflive.enums import MarketState, OptionType, QuoteType

class Quote:
    """
    The Quote object is provided for handling market data in a structured way.

    Quote instances are emitted in real-time as they are received from 
    Yahoo! Finance and offer a common interface for acquiring the data 
    provided.
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

        Parameters:
        -----------
        identifier: <type>
            Unique Yahoo! Finance identifier
        time: <type>
            Time of quote
        quoteType: <type>
            Type of underlying instrument
        kwargs:
            Additional quote information (limited by __fields__)
        """
        self._uuid = str(uuid.uuid4())

        for f in self.__fields__:
            setattr(self, f, kwargs.get(f))

        # Mandatory
        self.identifier = str(kwargs["identifier"]).upper()
        self.time = kwargs["time"]
        self.quoteType = QuoteType(kwargs["quoteType"])

        # Enum redeclaration
        self.marketState = MarketState(self.marketState)
        self.optionType = OptionType(self.optionType)

    def __str__(self): 
        return "{0} {1} - Price: {2}, {3} : {4}".format(
                    self.quoteType.name, self.identifier, 
                    self.price, self.exchange,
                    self.marketState.name
                )
        