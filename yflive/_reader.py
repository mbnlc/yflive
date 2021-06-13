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

from yflive.yfquote_pb2 import YFQuote
from yflive.quote import Quote

class _QuoteReader:
    """
    Reader class for Yahoo! Finance websocket messages.

    This class implements the logic needed to decrypt websocket messages sent
    by Yahoo! Finance.
    """

    def __init__(self, buf: List[int], pos: int, length: int):
        self.buf = buf
        self.pos = pos
        self.length = length

    # ==========================================================================
    # Parse Yahoo! Finance websocket message to Quote
    # ==========================================================================

    @staticmethod
    def parse(msg: str):
        """
        Parse Yahoo! Finance message to Quote object
        
        Parameters:
        -----------
        msg: str
            Yahoo! Finance base64 encoded quote string
        """
        message_bytes = base64.b64decode(msg)
        yfquote = YFQuote()
        yfquote.ParseFromString(message_bytes)

        fields = {}
        for f in _QuoteReader.available_fields(msg):
            fields[f] = getattr(yfquote, f, None)

        return Quote(**fields)

    @staticmethod
    def available_fields(msg: str): 
        """
        Get available fields from message

        Parameters:
        -----------
        msg: str
            Yahoo! Finance base64 encoded quote string
        """
        buffer = list(base64.b64decode(msg))
        reader = _QuoteReader(buffer, 0, len(buffer))
        c = reader.length
        available_fields = []
        while reader.pos < c:
            t = reader._uint32()
            available_fields.append(Quote.__fields__[(t >> 3) - 1])
            reader._skipType(t & 7)
        return available_fields

    # ==========================================================================
    # Helper methods
    # ==========================================================================    

    def _incr(self):
        self.pos += 1
        return self.pos - 1

    def _uint32(self):
        value = 4294967295
        value = (self.buf[self.pos] & 127) >> 0
        if (self.buf[self._incr()] < 128): 
            return value

        value = (value | (self.buf[self.pos] & 127) << 7) >> 0
        if (self.buf[self._incr()] < 128): 
            return value

        value = (value | (self.buf[self.pos] & 127) << 14) >> 0
        if (self.buf[self._incr()] < 128): 
            return value

        value = (value | (self.buf[self.pos] & 127) << 21) >> 0 
        if (self.buf[self._incr()] < 128): 
            return value

        value = (value | (self.buf[self.pos] &  15) << 28) >> 0 
        if (self.buf[self._incr()] < 128): 
            return value

        self.pos += 5
        if ((self.pos) > self.length):
            self.pos = self.length
        return value

    def _skip(self, length=None):
        if isinstance(length, int):
            if self.pos + length > self.length:
                return IndexError("index out of range")
            self.pos += length
        else:
            while True:
                if self.pos >= self.length:
                    return IndexError("index out of range")
                if self.buf[self._incr()] & 128 == 0:
                    break
        return

    def _skipType(self, wireType):
        if wireType == 0:
            self._skip()
        elif wireType == 1:
            self._skip(8)
        elif wireType == 2:
            self._skip(self._uint32())
        elif wireType == 3:
            wireType = self._uint32() & 7
            while wireType != 4:
                self._skipType(wireType)
                wireType = self._uint32() & 7
        elif wireType == 5:
            self._skip(4)
        else:
            return 
        return