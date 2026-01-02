# Batoto Parser

[![PyPI version](https://badge.fury.io/py/batoto-parser.svg)](https://badge.fury.io/py/batoto-parser)
[![Python versions](https://img.shields.io/pypi/pyversions/batoto-parser.svg)](https://pypi.org/project/batoto-parser/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lightweight parser for Batoto-style manga sites. Provides both a command-line interface (CLI) and a Python library for metadata extraction and chapter decryption.

## Features

- **CLI Tool**: Easy-to-use command-line interface with rich output
- **Python Library**: Import and use in your own projects
- **Flexible**: Works with any Batoto-style manga site
- **Fast**: Efficient parsing with minimal dependencies
- **Typed**: Full type hints for better IDE support

---

## 🚀 Quick Start

Get up and running in seconds.

### 1. Installation
```bash
pip install batoto-parser

# Search for a manga
batoto-parser list --query "one piece"

# Get chapter image links (Requires Node.js)
batoto-parser pages [https://bato.to/title/12345-title/67890-ch-1](https://bato.to/title/12345-title/67890-ch-1)
```

---

### Prerequisites & Node.js Alert (Very Important)

## ⚡ Prerequisites: Node.js Requirement

**Important:** To decrypt image URLs (the `pages` command), **Node.js** must be installed on your system. This tool uses Node to evaluate the site's decryption logic securely.

| OS | Command to Install |
| :--- | :--- |
| **Ubuntu/Debian** | `sudo apt install nodejs` |
| **Fedora/RHEL** | `sudo dnf install nodejs` |
| **Arch Linux** | `sudo pacman -S nodejs` |
| **MacOS** | `brew install node` |
| **Windows** | Download from [nodejs.org](https://nodejs.org/) |

---

## 🛠 CLI Commands Overview

The `batoto-parser` command provides several sub-commands. Use `--help` after any command for detailed flags.

| Command | Description | Common Flag |
| :--- | :--- | :--- |
| `list` | Browse or search for manga titles. | `--query "name"` |
| `details` | Fetch metadata and chapter lists for a series. | `--output file.json` |
| `pages` | Decrypt and list all image URLs for a chapter. | `--domain custom.com` |

### Advanced CLI Examples
```bash
# Browse specific page
batoto-parser list --page 2

# Save manga details to a JSON file
batoto-parser details /series/Some-Manga --output manga.json

# Use a different domain
batoto-parser list --domain custom-site.com --pretty
```

---

### Library Usage (For Developers)
## 📖 Library Usage

Integrate the parser directly into your Python scripts:

```python
from batoto_parser import BatoToParser, MangaLoaderContext

# Initialize context and parser
ctx = MangaLoaderContext()
parser = BatoToParser(ctx)

# Get details for a specific manga
manga = parser.get_details("/series/12345")
print(f"Title: {manga.title}")

# Fetch decrypted pages (Node.js required)
pages = parser.get_pages("/title/12345/67890")
for p in pages:
    print(f"Page {p.page_number}: {p.image_url}")
```

---

### Troubleshooting & Project Structure
## 🔧 Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **"Cannot evaluate batoPass"** | Node.js is missing or not in your system PATH. Install Node.js. |
| **Empty results** | The site may be using Cloudflare or the layout changed. Try a different `--domain`. |
| **Network errors** | Check your connection or use a VPN if the domain is blocked in your region. |

## 📂 Project Structure

```text
batoto-parser/
├── src/batoto_parser/   # Core logic (Parser, Models, CLI)
├── tests/               # Pytest suite
├── examples/            # Usage scripts
└── pyproject.toml       # Build system & dependencies
```

---

### Contributing, Changelog & Disclaimer

## 🤝 Contributing

Contributions are welcome! 

1. **Fork** the Project.
2. **Create** your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. **Run Tests** (`pytest`).
4. **Push** to the Branch and open a **Pull Request**.

## 📜 Changelog

Detailed changes for each release are documented in our [GitHub Releases](https://github.com/mehrinshamim/batoto-parser/releases) page.

* **v0.1.0**: Initial release (CLI + Library core).

## ⚖️ License & Disclaimer

**License:** Distributed under the [MIT License](LICENSE).

**Disclaimer:** This tool is for educational purposes only. Users are responsible for complying with the Terms of Service of any website they access. The authors are not responsible for any misuse.

---

**Maintained by:** [mehrinshamim/Org]
