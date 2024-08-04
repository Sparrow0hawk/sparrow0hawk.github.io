from pathlib import Path
from textwrap import dedent

import pytest

from blog.cli import execute


def test_execute(content: Path) -> None:
    content_path = str(content.absolute())
    output_dir = content.parent
    args = [content_path, str(output_dir)]

    execute(args)

    assert (output_dir / "site").exists()
    assert (output_dir / "site" / "index.html").exists()
    assert (output_dir / "site" / "posts" / "2024-08-01-hello_world.html").exists()


@pytest.fixture(name="content")
def content_fixture(tmp_path: Path) -> Path:
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    post = content_dir / "2024-08-01-hello_world.md"
    post.write_text(
        dedent(
            """
        # Hello world
        
        Hello world! This is a blog post!
        """
        )
    )
    return content_dir
