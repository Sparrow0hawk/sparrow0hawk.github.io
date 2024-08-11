from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from shutil import copytree

from jinja2 import Environment, FileSystemLoader

from blog.feed import Feed
from blog.post import Post

SCRIPT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))


def execute(args: list[str]) -> None:
    output_dir = Path(args[1]) / "site"
    output_dir.mkdir(exist_ok=True)
    posts_dir = output_dir / "posts"
    posts_dir.mkdir(exist_ok=True)

    content_path = Path(args[0])
    post_files = [path for path in content_path.iterdir() if path.is_file()]
    post_files.sort(reverse=True)
    posts = [Post.create(path=name.resolve()) for name in post_files]

    env = Environment(loader=FileSystemLoader(SCRIPT_DIR / "templates"), trim_blocks=True, lstrip_blocks=True)

    generate_index(output_dir, env, posts)
    for post in posts:
        generate_post(posts_dir, env, post)

    feed = Feed(title="Alex Coleman's blog", link="https://alexjcoleman.me/", author_name="Alex Coleman")
    feed.add_posts(*posts)

    with open(output_dir / "atom.xml", "w") as atom_feed:
        atom_feed.write(feed.build(datetime.now(UTC)))

    _copy_assets(output_dir)


def _copy_assets(output_dir: Path) -> None:
    copytree(SCRIPT_DIR / "assets", output_dir / "static", dirs_exist_ok=True)


def generate_post(post_dir: Path, env: Environment, post: Post) -> None:
    template = env.get_template("post.html")
    with open(post_dir / f"{post.filename}.html", "w") as post_file:
        post_file.write(template.render({"title": post.title, "content": post.content}))


def generate_index(output_dir: Path, env: Environment, posts: list[Post]) -> None:
    template = env.get_template("index.html")
    with open(output_dir / "index.html", "w") as html_file:
        html_file.write(template.render({"title": "Home", "posts": posts}))
