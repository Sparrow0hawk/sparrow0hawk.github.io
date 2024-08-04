from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def execute(args: list[str]) -> None:
    output_dir = Path(args[1]) / "site"
    (output_dir / "static").mkdir(parents=True, exist_ok=True)
    posts_dir = output_dir / "posts"
    posts_dir.mkdir(exist_ok=True)

    content_path = Path(args[0])
    post_files = [path for path in content_path.iterdir() if path.is_file()]
    post_files.sort(reverse=True)
    posts = [Post.create(path=name.resolve()) for name in post_files]

    env = Environment(
        loader=FileSystemLoader(os.path.join(SCRIPT_DIR, "templates")), trim_blocks=True, lstrip_blocks=True
    )

    generate_index(output_dir, env, posts)
    for post in posts:
        generate_post(posts_dir, env, post)


def generate_post(post_dir: Path, env: Environment, post: Post) -> None:
    template = env.get_template("post.html")
    with open(post_dir / f"{post.filename}.html", "w") as post_file:
        post_file.write(template.render({"title": post.title, "content": post.content}))


def generate_index(output_dir: Path, env: Environment, posts: list[Post]) -> None:
    template = env.get_template("index.html")
    with open(output_dir / "index.html", "w") as html_file:
        html_file.write(template.render({"title": "Home", "posts": posts}))


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
