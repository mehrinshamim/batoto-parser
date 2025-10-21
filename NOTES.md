# Batoto Python Parser — Notes & Changes

Branch: add-python-batoto-comments
Based on: add-python-batoto-parser

## Summary of work

- Added an initial Python reimplementation of the Batoto parser (synchronous) on branch `add-python-batoto-parser` and created a feature branch `add-python-batoto-comments` from it.
- Implemented scraping for: listing, details, chapters, and chapter page image URL extraction (including AES decrypt logic matching the Kotlin implementation).
- Extended the parser with comment/review parsing heuristics on `add-python-batoto-comments` and added a NOTES file documenting changes, concerns, and suggestions.

## Files added (on add-python-batoto-parser)
- requirements.txt
- models.py
- context.py
- utils.py
- bato_parser.py

## Files updated/added on add-python-bato-comments
- models.py (extended with Comment dataclass)
- context.py (extended with JSON helpers and cookie access)
- utils.py (added parse_relative_date_to_epoch_ms helper)
- bato_parser.py (added get_comments, _parse_comments_from_container, _parse_comments_json_object)
- NOTES.md (this file)

Exact file paths in repo branch `add-python-batoto-comments`:
- requirements.txt
- models.py
- context.py
- utils.py
- bato_parser.py
- NOTES.md

## What I implemented (behavior)

1. Core scraper (synchronous):
   - get_list(page, order, query): fetches browse/search pages and returns Manga objects with id, title, cover, tags, public URL.
   - get_details(manga): fetches manga details page and returns title, large cover, description HTML, genres, and list of chapters.
   - get_pages(chapter_url): fetches chapter page, finds inline JS variables (images array, batoPass, batoWord), evaluates batoPass via a JS engine (node subprocess), base64-decodes batoWord, derives key+IV using the same MD5-based EVP_BytesToKey style routine, decrypts AES-CBC to obtain per-image query args, and composes final image URLs.

2. Comments/Reviews parsing (new on add-python-batoto-comments):
   - get_comments(manga_url, page=1): attempts to parse comments using layered heuristics:
     - parse HTML comment containers if present (selectors like #comments, .comment-list, .review-list).
     - search inline scripts for embedded comment JSON or API endpoints and call XHR endpoints if detected.
     - fallback: detect any element with class containing "comment" and parse it.
   - _parse_comments_from_container: converts HTML comment nodes into Comment dataclass instances (author, content HTML/text, posted_at_ms, rating, likes, nested replies).
   - _parse_comments_json_object: converts common JSON comment shapes into Comment objects.

## How to test locally (quick steps)
1. Checkout the branch:
   git fetch origin add-python-batoto-comments
   git checkout add-python-batoto-comments

2. Create virtualenv and install deps:
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt

3. Ensure Node.js is installed and available in PATH (context.evaluate_js uses `node -e` to evaluate the small JS expression required by the site). If you prefer, later I can replace this with an embedded JS runtime.

4. Quick script example:

```python
from context import MangaLoaderContext
from bato_parser import BatoToParser

ctx = MangaLoaderContext()
parser = BatoToParser(ctx, domain="bato.to")

# list
mangas = parser.get_list(page=1)
print('found', len(mangas))

# details (use one of the returned mangas or the provided example)
# manga = mangas[0]
manga = Manga(id='', title='', url='/series/83624', public_url='https://bato.to/series/83624', alt_titles=set(), cover_url=None, large_cover_url=None, description_html=None, tags=[], state=None, authors=set())
details = parser.get_details(manga)
print(details.title)

# comments
comments = parser.get_comments('/series/83624')
print('comments:', len(comments))

# pages (for a chapter)
# pages = parser.get_pages('/chapter/123456')
# print('pages', len(pages))
```

## Concerns, caveats & suggestions (things to note)

- Node dependency: the provided MangaLoaderContext.evaluate_js uses a node subprocess. Node must be installed on the host. This is a simple approach for now but has overhead. Alternatives:
  - Embed a JS engine (PyMiniRacer, quickjs, v8 bindings) to evaluate JS more efficiently.
  - Extract password computation from page if it is a simple expression and avoid running node for every chapter by caching evaluated expressions when possible.

- AES decryption / key derivation: the Kotlin code uses an MD5-based loop (EVP_BytesToKey-like) to derive key+IV. The Python implementation reproduces this. Keep in mind:
  - The code expects OpenSSL "Salted__" prefix in the base64 blob.
  - Use pycryptodome or cryptography for AES-CBC decryption. The current code uses pycryptodome.

- HTML structure fragility: the parser relies on specific CSS selectors and inline JS names (imgHttps, batoPass, batoWord, etc.). If the site changes markup or obfuscation names, the parser will break and need updates.

- Authentication: the current implementation does not perform interactive login. To support authenticated-only comments or gated content, we need to:
  - Add a login flow (post credentials or use a browser/webview and import cookies into requests.Session), or
  - Allow the user to provide a cookie jar or cookies exported from a logged-in browser.

- Rate-limiting and politeness: implement throttling and retry/backoff for production scraping to avoid IP bans.

- Tests & CI: add unit tests for the decrypt routine, parse helpers, and parsing of representative saved HTML fixtures to quickly detect breakages when the site changes.

- Async migration: later, converting the client to async (aiohttp) will improve throughput for bulk scraping but is not required now. We'll confirm parsing correctness synchronously first (as you requested).

## Next steps (after this commit)

- I will push this NOTES.md to branch `add-python-batoto-comments` (this commit).
- After pushing, I will run a test against https://bato.to/series/83624 to verify comment parsing and refine selectors / XHR detection. If necessary I will update the parser with site-specific logic.
- We will NOT convert to async yet — we will verify synchronous implementation first, then migrate to async if needed.

---

If you want any section reworded, or additional items added to NOTES (examples, license note, test results), tell me and I will update the file on the same branch.