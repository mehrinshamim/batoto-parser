from dataclasses import dataclass
from typing import List, Optional, Set

@dataclass(frozen=True)
class MangaTag:
    title: str
    key: str
    
@dataclass
class Manga:
    id: str
    title: str
    alt_titles: Set[str]
    url: str            # relative url as in site
    public_url: str     # absolute url
    cover_url: Optional[str]
    large_cover_url: Optional[str]
    description_html: Optional[str]
    tags: List[MangaTag]
    state: Optional[str]
    authors: Set[str]

@dataclass
class MangaChapter:
    id: str
    title: Optional[str]
    number: float
    url: str
    scanlator: Optional[str]
    upload_date_ms: int

@dataclass
class MangaPage:
    id: str
    url: str
    preview: Optional[str]
