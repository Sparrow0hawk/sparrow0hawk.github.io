from datetime import datetime
from pathlib import Path
from textwrap import dedent

from blog.post import Post


def test_init() -> None:
    post = Post(
        filename="2024-08-01-hello_world",
        title="01 Aug 2024 Hello World",
        content="<h1>Hello world!</h1>",
        publish_date=datetime(2024, 8, 1, 12)
    )

    assert (
            post.filename == "2024-08-01-hello_world"
            and post.title == "01 Aug 2024 Hello World"
            and post.content == "<h1>Hello world!</h1>"
            and post.publish_date == datetime(2024, 8, 1, 12)
    )


def test_create(tmp_path: Path) -> None:
    post_path = tmp_path / "2024-08-01-hello_world.md"
    post_path.write_text(dedent(
        """
        # Hello World
        
        Hello world!
        """
    ))

    post = Post.create(path=post_path)

    assert (
            post.filename == "2024-08-01-hello_world"
            and post.title == "01 Aug 2024 Hello World"
            and post.content == "<h1>Hello World</h1>\n<p>Hello world!</p>"
            and post.publish_date == datetime(2024, 8, 1)
    )
