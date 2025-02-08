# Personal site

This repository is for my personal site.

## Setup

To build the site you will need:
- Python3.12
- GNU Make

1. Create a virtual environment
   ```bash
   python3.12 -m venv --prompt . --upgrade-deps .venv
   ```
2. Install dependencies
   ```bash
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```
3. Build site
   ```bash
   RELATIVE=1 make html
   ```
4. Serve site
   ```bash
   make serve
   ```
