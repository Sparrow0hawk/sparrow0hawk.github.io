from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import markdown


@dataclass
class Post:
    filename: str
    title: str
    path: Path
    content: str

    @classmethod
    def create(cls, path: Path) -> Post:
        with open(path) as markdown_post:
            post_content = markdown_post.read()
            converted_post = markdown.markdown(post_content, extensions=["fenced_code"])
        post_title = next(line for line in post_content.splitlines() if line.startswith("#"))
        return Post(
            title=cls._title(filename=path.stem, post_title=post_title),
            path=path,
            content=converted_post,
            filename=path.stem,
        )

    @staticmethod
    def _title(filename: str, post_title: str) -> str:
        year, month, day, *_ = filename.split("-")
        post_date = date(year=int(year), month=int(month), day=int(day))

        title = f"{post_date.strftime('%d %b %Y')} {post_title.replace('# ', '')}"
        return title
