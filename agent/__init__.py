# Copyright (c) Trainline Limited, 2016. All rights reserved. See LICENSE.txt in the project root for license information.

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
