import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

CHECKMARK = "  \u2705"
DISABLED = "\033[31m(Disabled)\033[0m"
ENABLED = "\033[32m(Enabled)\033[0m"
