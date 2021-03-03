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