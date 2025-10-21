#!/usr/bin/env python3

from context import MangaLoaderContext
from bato_parser import BatoToParser
from bs4 import BeautifulSoup

URL = "https://bato.to/series/83624"

def dump_page_scripts(html):
    soup = BeautifulSoup(html, "lxml")
    scripts = soup.find_all("script")
    print(f"Found {len(scripts)} <script> tags")
    for i, s in enumerate(scripts[:30]):
        text = s.string or ""
        snippet = text.strip().replace('\n', ' ')[:400]
        print(f"--- script[{i}] (len={{len(text)}}): {{snippet!r}}\n")


def main():
    ctx = MangaLoaderContext()
    print("Fetching page:", URL)
    resp = ctx.http_get(URL)
    print("HTTP status:", resp.status_code)
    dump_page_scripts(resp.text)

    parser = BatoToParser(ctx, domain="bato.to")
    print("Calling parser.get_comments()...")
    try:
        comments = parser.get_comments('/series/83624')
        print(f"Parsed {len(comments)} comments")
        for i, c in enumerate(comments[:10]):
            print(f"--- Comment {{i}} ---")
            print("author:", c.author)
            print("posted_at_ms:", c.posted_at_ms)
            print("rating:", c.rating)
            print("likes:", c.likes)
            print("content_text:", c.content_text[:200])
    except Exception as e:
        print("get_comments raised:", repr(e))

if __name__ == '__main__':
    main()