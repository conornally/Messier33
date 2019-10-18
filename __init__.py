from Messier33.src.log import *
log = Logging(2)
from Messier33.include.m33 import *
from Messier33.include.config import *
from Messier33.src.catalog import Catalog
from Messier33.src import fileio as io
from Messier33.src.loading import Loading
import Messier33.src.mask as mask

import Messier33.include.pandas_config as pandas_config

def log_level(level): log.set_level(level)
def debug(message): log.debug(message)
def info(message): log.info(message)
def warn(message): log.warn(message)
#log_level(1)



