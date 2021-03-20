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

import base64
import struct

from yflive.quote import Quote
from yflive.asset_class import AssetClass
from yflive.market_state import MarketState

class QuoteReader:
    """
    Reader class for yahoo!finance websocket messages.

    This class implements the logic needed to decrypt websocket messages sent
    by yahoo!finance.
    """

    def __init__(self, buf: List[int], pos: int, length: int):
        self.buf = buf
        self.pos = pos
        self.length = length

    def incr(self):
        self.pos += 1
        return self.pos - 1

    def uint32(self):
        value = 4294967295
        value = (self.buf[self.pos] & 127) >> 0
        if (self.buf[self.incr()] < 128): 
            return value

        value = (value | (self.buf[self.pos] & 127) << 7) >> 0
        if (self.buf[self.incr()] < 128): 
            return value

        value = (value | (self.buf[self.pos] & 127) << 14) >> 0
        if (self.buf[self.incr()] < 128): 
            return value

        value = (value | (self.buf[self.pos] & 127) << 21) >> 0 
        if (self.buf[self.incr()] < 128): 
            return value

        value = (value | (self.buf[self.pos] &  15) << 28) >> 0 
        if (self.buf[self.incr()] < 128): 
            return value

        self.pos += 5
        if ((self.pos) > self.length):
            self.pos = self.length
        return value

    def read_bytes(self):
        length = self.uint32()
        start = self.pos
        end = self.pos + length

        self.pos += length
        return self.buf[start:end]

    def read_string(self):
        b = self.read_bytes()
        return "".join(map(chr, b))

    def read_float(self):
        start = self.pos
        self.pos += 4
        b = bytearray(self.buf[start:self.pos])
        return struct.unpack('f', b)[0]

    def read_int32(self):
        return self.uint32() | 0

    def skip(self, length=None):
        if isinstance(length, int):
            if self.pos + length > self.length:
                return IndexError("index out of range")
            self.pos += length
        else:
            while True:
                if self.pos >= self.length:
                    return IndexError("index out of range")
                if self.buf[self.incr()] & 128 == 0:
                    break
        return

    def skipType(self, wireType):
        if wireType == 0:
            self.skip()
        elif wireType == 1:
            self.skip(8)
        elif wireType == 2:
            self.skip(self.uint32())
        elif wireType == 3:
            wireType = self.uint32() & 7
            while wireType != 4:
                self.skipType(wireType)
                wireType = self.uint32() & 7
        elif wireType == 5:
            self.skip(4)
        else:
            return 
        return

    # ==========================================================================
    # Parse yahoo!finance websocket msg to Quote
    # ==========================================================================

    @staticmethod
    def parse(message):
        """
        Decodes yahoo!finance websocket message using the QuoteReader class.
        """

        buffer = list(base64.b64decode(message))
        reader = QuoteReader(buffer, 0, len(buffer))
        c = reader.length
        new_quote = Quote()
        while reader.pos < c:
            t = reader.uint32()
            if (t >> 3) == 1:       # Read id
                new_quote.identifier = str(reader.read_string())
            elif (t >> 3) == 2:     # Read price
                new_quote.price = float(reader.read_float())
            elif (t >> 3) == 5:     # Read exchange
                new_quote.exchange = str(reader.read_string())
            elif (t >> 3) == 6:     # Read quoteType
                new_quote.asset_class = AssetClass(reader.read_int32())
            elif (t >> 3) == 7:     # Read market_hours
                new_quote.market_state = MarketState(reader.read_int32())
            else:                   # Value not found
                reader.skipType(t & 7)
        return new_quote