import pymongo

from session import Session
from metadata import Field, Index, collection
from declarative import Document
from base import Cursor
from version import __version__, __version_info__
from config import configure

# Re-export direction keys
ASCENDING = pymongo.ASCENDING
DESCENDING = pymongo.DESCENDING

