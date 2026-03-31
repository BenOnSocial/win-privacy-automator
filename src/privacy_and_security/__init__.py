import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(name)s: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
