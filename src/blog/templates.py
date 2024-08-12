from __future__ import annotations

import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from blog.post import Post

SCRIPT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))


class TemplateEngine:
    def __init__(self) -> None:
        self.env = Environment(loader=FileSystemLoader(SCRIPT_DIR / "templates"), trim_blocks=True, lstrip_blocks=True)

    def generate_index(self, posts: list[Post]) -> str:
        template = self.env.get_template("index.html")
        return template.render({"title": "Home", "posts": posts})
