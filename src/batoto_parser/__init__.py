"""
Batoto Parser - Lightweight parser for Batoto-style manga sites.

This package provides:
- Listing/browsing manga
- Fetching manga details and metadata
- Retrieving chapter pages with image URL decryption

Can be used as a library or CLI tool.
"""

from batoto_parser.__version__ import __version__
from batoto_parser.context import MangaLoaderContext
from batoto_parser.models import Manga, MangaChapter, MangaPage, MangaTag
from batoto_parser.parser import BatoToParser
from batoto_parser.utils import decrypt_batoto, evp_bytes_to_key, generate_uid

__all__ = [
    "__version__",
    "BatoToParser",
    "MangaLoaderContext",
    "Manga",
    "MangaChapter",
    "MangaPage",
    "MangaTag",
    "generate_uid",
    "decrypt_batoto",
    "evp_bytes_to_key",
]
