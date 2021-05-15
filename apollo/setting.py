import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
DATEF1 = "%Y%m%d"
DATEF2 = "%Y/%m/%d"
DATESTAMP1 = datetime.now().strftime(DATEF1)
DATESTAMP2 = datetime.now().strftime(DATEF2)
TIMEF1 = "%Y%m%d_%H%M%S"
TIMEF2 = "%Y%m%d_%a_%I%M%S_%p"
TIMESTAMP1 = datetime.now().strftime(TIMEF1)
TIMESTAMP2 = datetime.now().strftime(TIMEF2)

FORMATTER = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(FORMATTER)

# logfilename = os.path.join(LOG_DIR, DATESTAMP1+ ".log")
# file_handler = logging.FileHandler(logfilename, encoding="UTF-8")
# file_handler.setFormatter(FORMATTER)

file_handler = logging.handlers.RotatingFileHandler("apollo.log", maxBytes=5*1024*1024, backupCount=1,encoding="UTF-8")
file_handler.setFormatter(FORMATTER)

logging.getLogger('').addHandler(console_handler)
logging.getLogger('').addHandler(file_handler)
logging.getLogger('').setLevel(logging.INFO)