"""
modio is a python wrapper to interact with the mod.io API.
"""

#ToDo
# - change unix timestamp to datetime.datetime
# - make documentation lists better
# - make more use of enums?
# - less kwargs more named arguments

from .client import Client
from .objects import NewMod, NewModFile, Object, Filter
from .enums import *
from .errors import *

__version__ = "0.2.0"
