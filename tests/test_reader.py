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

import unittest

from yflive.quote import Quote
from yflive._reader import QuoteReader

from yflive.enums.price_hint import PriceHint
from yflive.enums.market_state import MarketState
from yflive.enums.quote_type import QuoteType

class TestReader(unittest.TestCase):
    """"""

    def test_available_fields(self):
        msg = "CgRUU0xBFR8FKUQYoMyD1ZVeKgNOTVMwCDgBRSLND8BIpvnwDmXAo3jB2AEE"
        fields = QuoteReader.available_fields(msg)

        should_contain = set(["identifier", "time", "quoteType", "marketState",
                          "priceHint", "exchange", "dayVolume", "price", 
                          "change", "changePercent"])

        self.assertSetEqual(set(fields), should_contain)

    def test_parse(self):
        msg = "CgRUU0xBFR8FKUQYoMyD1ZVeKgNOTVMwCDgBRSLND8BIpvnwDmXAo3jB2AEE"
        quote = QuoteReader.parse(msg)

        self.assertEqual(quote.identifier, "TSLA")
        self.assertEqual(quote.time, 1617815434000)
        self.assertEqual(quote.quoteType, QuoteType.EQUITY)
        self.assertEqual(quote.marketState, MarketState.REGULAR)
        self.assertEqual(quote.priceHint, PriceHint.BUY)

        self.assertEqual(quote.exchange, "NMS")
        self.assertEqual(quote.dayVolume, 15605331)

        self.assertAlmostEqual(quote.price, 676.0800170898438)
        self.assertAlmostEqual(quote.change, -15.53997802734375)
        self.assertAlmostEqual(quote.changePercent, -2.2468953132629395)


if __name__ == '__main__':
    unittest.main()