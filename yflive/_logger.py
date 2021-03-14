import logging

_logger = logging.getLogger("yflive")

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

_logger.addHandler(NullHandler())