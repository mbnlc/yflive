# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

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