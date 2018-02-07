from .bytecode import BFError

from .bytecode import Bytecode

from .pure import run as pure_run

import pyximport; pyximport.install()
from .cyt import run as cyt_run

