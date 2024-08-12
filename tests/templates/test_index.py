from datetime import datetime

from blog.post import Post
from blog.templates import TemplateEngine


def test_index() -> None:
    template_engine = TemplateEngine()
    posts = [
        Post(
            filename="2024-08-01-hello_world",
            title="Hello World",
            content="Hello world!",
            publish_date=datetime(2024, 8, 1),
        ),
        Post(
            filename="2024-08-02-hello_world_again",
            title="Hello World again!",
            content="Hello world!",
            publish_date=datetime(2024, 8, 2),
        ),
    ]
    index = template_engine.generate_index(posts)

    assert "<h1>My Blog</h1>" in index
