import argparse
import json
from urllib.parse import urljoin
from context import MangaLoaderContext
from bato_parser import BatoToParser
from models import Manga
from utils import generate_uid

def to_json(obj):
    def conv(o):
        if isinstance(o, set):
            return list(o)
        return o.__dict__ if hasattr(o, "__dict__") else str(o)
    return json.dumps(obj, default=conv, indent=2)

def make_min_manga(url, domain="bato.to"):
    rel = url
    if url.startswith("http"):
        # convert to relative-ish path for parser.abs behavior
        parsed = url.split(f"https://{domain}")[-1]
        rel = parsed or url
    return Manga(
        id=generate_uid(rel),
        title="",
        alt_titles=set(),
        url=rel,
        public_url=urljoin(f"https://{domain}", rel),
        cover_url=None,
        large_cover_url=None,
        description_html=None,
        tags=[],
        state=None,
        authors=set(),
    )

def cmd_list(args, parser):
    mangas = parser.get_list(page=args.page, order=args.order, query=args.query)
    print(to_json(mangas))

def cmd_details(args, parser):
    m = make_min_manga(args.manga_url, domain=parser.domain)
    details = parser.get_details(m)
    print(to_json(details))

def cmd_pages(args, parser):
    pages = parser.get_pages(args.chapter_url)
    print(to_json(pages))

def main():
    ap = argparse.ArgumentParser(description="Run bato-parser actions")
    ap.add_argument("--domain", default="bato.to")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s_list = sub.add_parser("list")
    s_list.add_argument("--page", type=int, default=1)
    s_list.add_argument("--order", default="update.za")
    s_list.add_argument("--query", default=None)

    s_details = sub.add_parser("details")
    s_details.add_argument("manga_url")

    s_pages = sub.add_parser("pages")
    s_pages.add_argument("chapter_url")

    args = ap.parse_args()
    ctx = MangaLoaderContext()
    parser = BatoToParser(ctx, domain=args.domain)

    if args.cmd == "list":
        cmd_list(args, parser)
    elif args.cmd == "details":
        cmd_details(args, parser)
    elif args.cmd == "pages":
        cmd_pages(args, parser)

if __name__ == "__main__":
    main()