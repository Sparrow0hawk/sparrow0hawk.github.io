from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import markdown


@dataclass
class Post:
    filename: str
    title: str
    content: str
    publish_date: datetime

    @classmethod
    def create(cls, path: Path) -> Post:
        with open(path) as markdown_post:
            post_content = markdown_post.read()
            converted_post = markdown.markdown(post_content, extensions=["fenced_code"])
        post_title = next(line for line in post_content.splitlines() if line.startswith("#"))
        publish_date = cls._parse_post_date(filename=path.stem)
        return Post(
            title=cls._title(post_date=publish_date, post_title=post_title),
            content=converted_post,
            filename=path.stem,
            publish_date=publish_date
        )

    @staticmethod
    def _title(post_date: datetime, post_title: str) -> str:
        return f"{post_date.strftime('%d %b %Y')} {post_title.replace('# ', '')}"

    @staticmethod
    def _parse_post_date(filename: str) -> datetime:
        year, month, day, *_ = filename.split("-")
        return datetime(year=int(year), month=int(month), day=int(day))
