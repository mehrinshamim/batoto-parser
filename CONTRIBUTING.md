# Contributing to batoto-parser

Thank you for your interest in contributing to **batoto-parser**! 🎉  
This project aims to provide a clean, reliable, and well-typed parser for Batoto-style manga sites, usable both as a CLI tool and a Python library.

Contributions of all kinds are welcome: bug fixes, improvements, documentation, and new features.

---

## ⚠️ Important Notes Before Contributing

- This project is **for educational purposes only**
- Contributors must respect website Terms of Service and `robots.txt`
- Do **not** add features intended to bypass paywalls, authentication, or anti-bot protections
- Avoid hardcoding site-specific secrets or credentials

---

## Ways to Contribute

You can help by:

- 🐛 Fixing parsing bugs when site layouts change
- 🧪 Improving or adding tests
- ✨ Enhancing CLI UX or library API ergonomics
- 🧠 Improving decryption or parsing robustness
- 📚 Improving documentation or examples
- 🔍 Adding support for additional Batoto-style sites (when feasible)

---

## Development Setup

### Prerequisites

- **Python 3.8+**
- **Node.js** (required for chapter image URL decryption)
- Git

Verify Node.js is available:
```bash
node --version
```

### Clone the Repository
```bash
git clone https://github.com/mehrinshamim/batoto-parser.git
cd batoto-parser
```

### Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Install Development Dependencies
```bash
pip install -e ".[dev]"
```
This installs:

+ testing tools
+ linters
+ type checkers
+ formatting tools

Project Structure
```bash
batoto-parser/
├── src/batoto_parser/
│   ├── cli.py         # Typer-based CLI
│   ├── parser.py     # Core parsing logic
│   ├── context.py    # HTTP session & JS evaluation
│   ├── models.py     # Typed data models
│   └── utils.py      # Crypto & helper utilities
├── tests/            # Unit & integration tests
├── examples/         # Usage examples
└── pyproject.toml
```

## Architecture Guidelines
+ Keep site/network logic inside context.py
+ Keep HTML parsing logic inside parser.py
+ Keep crypto / JS-related logic isolated in utils.py
+ Do not mix CLI concerns into core parser logic
+ Avoid breaking public APIs without discussion

## Running Tests
### All Tests
```bash
pytest
```
### With Coverage
```bash
pytest --cov=batoto_parser --cov-report=html
```
### Skip Integration Tests
```bash
pytest -m "not integration"
```
### Code Quality & Style
Before submitting a PR, please run:

+ Formatting
```bash
black src/ tests/
```
+ Linting
```bash
ruff check src/ tests/
```
+ Type Checking
```bash
mypy src/
```
***All checks should pass before opening a Pull Request.***

## Working With Site Changes
Batoto-style sites may change layouts frequently. If fixing parsing issues:

* Update selectors carefully
* Add or update tests when possible
* Avoid overly fragile selectors
* Handle missing or malformed data gracefully
* If parsing returns empty results:
* Verify the site is accessible
* Check selectors against current HTML
* Ensure no network or rate-limit issues
* Adding or Modifying CLI Commands
* Use Typer conventions
* Keep output machine-readable by default
* Preserve JSON output compatibility
* Avoid breaking existing flags or options

## Submitting a Pull Request

### Fork the repository
### Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```
### Make your changes
### Run tests and checks
### Commit with a clear message:
```bash
git commit -m "Add: short description of change"
```
### Push your branch:
```bash
git push origin feature/your-feature-name
```
### Open a Pull Request on GitHub
### Commit Message Guidelines
Use clear, descriptive messages:
+ Fix: handle empty chapter list
+ Add: support saving pages output to file
+ Improve: robustness of decryption logic
+ Refactor: simplify parser context handling

### Reporting Issues
When reporting bugs, please include:

+ Command or code snippet used
+ Target domain
+ Expected vs actual behavior
+ Stack traces or error messages (if any)
+ Avoid reporting issues related to:
+ Site blocks or bans
+ Login-only or paywalled content

### Code of Conduct
By contributing, you agree to uphold respectful and constructive communication. Harassment or abusive behavior will not be tolerated.

### Questions or Help
+ Open an Issue for bugs or feature requests
+ Use Discussions for questions or design ideas
+ Check existing issues before opening a new one

Thank you for contributing to batoto-parser ❤️