from __future__ import annotations
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader


def main() -> None:
    os.makedirs("site/static", exist_ok=True)

    content_path = Path("content")
    post_files = [path for path in content_path.iterdir() if path.is_file()]
    post_files.sort(reverse=True)
    posts = [Post(title=name.stem, path=name.resolve()) for name in post_files]

    env = Environment(
        loader=FileSystemLoader("templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )

    generate_index(env, posts)
    os.makedirs("site/posts", exist_ok=True)
    for post in posts:
        template = env.get_template("post.html")
        with open(post.path) as markdown_post:
            post_content = markdown_post.read()

        with open(f"site/posts/{post.title}.html","w") as post_file:
            converted_post = markdown.markdown(post_content)
            post_file.write(template.render({"title": post.title, "content": converted_post}))


def generate_index(env: Environment, posts: list[Post]) -> None:
    template = env.get_template("index.html")
    with open("site/index.html", "w") as html_file:
        html_file.write(template.render({"title": "Home", "posts": posts}))


@dataclass
class Post:
    title: str
    path: Path



if __name__ == "__main__":
    main()
