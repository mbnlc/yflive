from enum import Enum

class MarketState(Enum):
    """
    The MarketState shows what state the instruments market currently assumes.
    """

    PRE              = 0
    REGULAR          = 1
    POST             = 2
    EXTENDED         = 3
    UNDEFINED        = None