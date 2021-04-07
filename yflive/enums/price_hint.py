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

from enum import Enum

class PriceHint(Enum):
    """
    The PriceHint gives a recommendation of 5 different actions.

    Yahoo! Finance provides this recommendation on their webpage as a simple
    indicator for retail investors to buy, sell or hold the stock.

    The PriceHint changes rarely.
    """

    UNDEFINED           = 0
    STRONG_BUY          = 1
    BUY                 = 2
    HOLD                = 3
    UNDER_PERFORM       = 4
    SELL                = 5
    NONE                = None