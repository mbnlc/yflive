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

class AssetClass(Enum):
    """
    The AssetClass indicates the type of financial instrument represented by a
    quote.

    Depending on the AssetClass, a Quote might contain different data,
    thus the AssetClass is used for communicating what should be expected in 
    a Quote. 
    
    Something to watch out for, is that yahoo finance only offers delayed 
    quotes for certain AssetClasses.
    """

    UNDEFINED       = 0
    ALTSYMBOL       = 5
    HEARTBEAT       = 7
    EQUITY          = 8
    INDEX           = 9
    MUTUALFUND      = 11
    MONEYMARKET     = 12
    OPTION          = 13
    CURRENCY        = 14
    WARRENT         = 15
    BOND            = 17
    FUTURE          = 18
    ETF             = 20
    COMMODITY       = 23
    ECNQUOTE        = 28
    CRYPTOCURRENCY  = 41
    INDICATOR       = 42
    INDUSTRY        = 1000
    NONE            = None