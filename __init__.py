from Messier33.src.log import Logging

global log_level
log_level=2
def debug(msg):
    print("init%d"%log_level)
    Logging(log_level).debug(msg)
def info(msg):Logging(log_level).info(msg)
def warn(msg):Logging(log_level).warn(msg)

from Messier33.include.m33 import *
from Messier33.include.config import *
from Messier33.src.catalog import Catalog
from Messier33.src import fileio as io
from Messier33.src.loading import Loading
import Messier33.src.mask as mask
import Messier33.include.pandas_config as pandas_config




