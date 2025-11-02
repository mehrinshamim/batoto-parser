# batoto-parser

Lightweight parser for Batoto-style manga sites. Provides:
- Listing (browse/search)
- Manga details (metadata + chapters)
- Chapter pages (decodes encrypted batoWord to produce image URLs)

## Requirements (Linux)
- Python 3.8+
- Node.js on PATH (required for JS evaluation when fetching pages)
- Python packages:
  - requests
  - beautifulsoup4
  - lxml
  - pycryptodome

Install deps:
```bash
# optional: create venv
python3 -m venv .venv
source .venv/bin/activate

pip install requests beautifulsoup4 lxml pycryptodome

# ensure node is installed:
# Debian/Ubuntu:
sudo apt update && sudo apt install -y nodejs
```

## Files of interest
- bato_parser.py — main parser (BatoToParser)
- context.py — HTTP session + JS eval helper (MangaLoaderContext)
- utils.py — crypto helpers (evp_bytes_to_key, decrypt_batoto), generate_uid
- models.py — dataclasses (Manga, MangaChapter, MangaPage, MangaTag)
- run_parser.py — CLI that prints JSON to stdout
- test_runner.py — CLI that writes JSON output to file (default `out.json`)

## Quick usage

From repository root.

1) List (browse/search)
- Print to stdout:
  ```bash
  python3 run_parser.py list --page 1
  python3 run_parser.py list --page 1 --query "one piece"
  ```
- Save to file (redirect):
  ```bash
  python3 run_parser.py list --page 1 > out.json
  ```

2) Manga details
- Print:
  ```bash
  python3 run_parser.py details /series/Some-Manga
  python3 run_parser.py details https://bato.to/series/Some-Manga
  ```
- Save:
  ```bash
  python3 run_parser.py details https://bato.to/series/Some-Manga > out.json

  ```

3) Chapter pages (requires node)
- Print:
  ```bash
  python3 run_parser.py pages /reader/12345
  ```
- Save:
  ```bash
  python3 run_parser.py pages /reader/12345 > out.json
  ```


## Notes & troubleshooting
- If get_pages fails with "Cannot evaluate batoPass" or returns null data, ensure `node` is installed and on PATH.
- If HTML parsing returns empty results, the site layout may have changed — update selectors in `bato_parser.py`.
- Network errors are not heavily retried; consider adding timeouts/retries in `context.py`.
- Decryption uses OpenSSL-style EVP_BytesToKey + AES-CBC; errors may indicate encoding or password problems.

## Next steps (suggestions)
- Add logging and configurable timeouts/retries.
- Add unit tests for crypto functions and JS evaluation stub.
- Harden error handling and add rate-limiting/backoff for production use.