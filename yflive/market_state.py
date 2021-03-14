from enum import Enum

class MarketState(Enum):
    """
    The MarketState shows what state the instruments market currently assumes.

    Notice that this does not include a "CLOSED" market state. This is because 
    quotes are not emitted when the underlying market is closed / when no 
    trading occures.
    """

    PRE              = 0
    REGULAR          = 1
    POST             = 2
    EXTENDED         = 3
    UNDEFINED        = None