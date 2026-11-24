## Prerequisites

The documentation toolchain requires **Python 3.10+** and **Sphinx** with the **Furo** theme.

## Python Environment Setup

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Building the Documentation

### Single Build

Build the HTML documentation once (from inside the `docs/` directory):

```bash
python -m sphinx -b html . _build/html
```

### Live Reload Preview (Development)

To rebuild automatically when documentation files change and preview the site with live reload, run:

```bash
sphinx-autobuild . _build/html
```

The preview server is available at <http://127.0.0.1:8000> by default. Stop it with `Ctrl+C`.
