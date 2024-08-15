from datetime import datetime

from bs4 import BeautifulSoup

from blog.post import Post
from blog.templates import TemplateEngine


class PostPage:
    def __init__(self, page: str):
        self.soup = BeautifulSoup(page, "html.parser")
        title = self.soup.select_one("title")
        assert title
        self.title = (title.string or "")
        heading = self.soup.select_one("body h1")
        paragraph = self.soup.select_one("body p")
        assert heading
        assert paragraph
        self.heading = (heading.string or "")
        self.paragraph = (paragraph.string or "")

def test_post_has_title() -> None:
    template_engine = TemplateEngine()
    post = Post(
            filename="2024-08-01-hello_world",
            title="Hello World",
            content="<h1>Hello world!</h1>\n<p>This is the beginning!</p>",
            publish_date=datetime(2024, 8, 1),
        )

    post_str = template_engine.generate_post(post)

    post_page = PostPage(post_str)

    assert post_page.title == "Hello World"


def test_post_has_content() -> None:
    template_engine = TemplateEngine()
    post = Post(
            filename="2024-08-01-hello_world",
            title="Hello World",
            content="<h1>Hello world!</h1>\n<p>This is the beginning!</p>",
            publish_date=datetime(2024, 8, 1),
        )

    post_str = template_engine.generate_post(post)

    post_page = PostPage(post_str)

    assert post_page.heading == "Hello world!"
    assert post_page.paragraph == "This is the beginning!"
