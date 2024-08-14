from __future__ import annotations

from datetime import datetime
from typing import Iterator, Any

from bs4 import BeautifulSoup, Tag

from blog.post import Post
from blog.templates import TemplateEngine


class IndexPage:
    def __init__(self, page: str):
        self.soup = BeautifulSoup(page, "html.parser")
        heading = self.soup.select_one("h1")
        assert heading
        self.heading = heading.string or ""
        posts = self.soup.select_one("ul")
        assert posts
        self.posts = IndexPostListComponent(posts)


class IndexPostListComponent:
    def __init__(self, list_: Tag):
        self.list = list_

    def __iter__(self) -> Iterator[IndexPostItemComponent]:
        return (IndexPostItemComponent(item) for item in self.list.select("li"))

    def __call__(self, *args: Any, **kwargs: Any) -> list[dict[str, str | list[str]]]:
        return [{"link": item.link, "text": item.text} for item in self]


class IndexPostItemComponent:
    def __init__(self, list_item: Tag):
        anchor = list_item.select_one("a")
        assert anchor
        # this could be a list[str]
        self.link = anchor["href"]
        self.text = anchor.string or ""


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
    index_page = IndexPage(index)

    assert index_page.heading == "My Blog"
    assert index_page.posts() == [
        {"link": "posts/2024-08-01-hello_world.html", "text": "01 Aug 2024 Hello World"},
        {"link": "posts/2024-08-02-hello_world_again.html", "text": "02 Aug 2024 Hello World again!"},
    ]
