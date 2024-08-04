# Personal site

This repository is for my personal site.

## Setup

To build the site you will need:
- Python3.12

1. Create a virtual environment
   ```bash
   python3.12 -m venv --prompt . --upgrade-deps .venv
   ```
2. Install dependencies
   ```bash
   source .venv/bin/activate
   
   pip install .
   ```
3. Run generate script
   ```bash
   python -m blog content .
   ```
4. Serve site
   ```bash
   python -m http.server -d site/ 8000
   ```
