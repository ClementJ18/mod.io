"""
modio is a python wrapper to interact with the mod.io API.
"""

from .client import Client
from .objects import NewMod, NewModFile, Object, Filter
from .enums import *
from .errors import *

__version__ = "0.4.2"
