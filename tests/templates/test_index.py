from __future__ import annotations

from datetime import datetime
from random import sample
from typing import Any, Iterator

import pytest
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
        footer = self.soup.select_one("footer")
        assert footer
        self.footer = FooterComponent(footer)


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

class FooterComponent:
    def __init__(self, footer: Tag):
        links = footer.select("a")
        assert links
        self.rss = links[0]
        self.mastodon = links[1]

    def __call__(self) -> dict[str, str | list[str]]:
        # indexing ResultSet[Tag] could be str | list[str]
        return {"RSS": self.rss["href"], "Mastodon": self.mastodon["href"]}

def test_index_has_title() -> None:
    template_engine = TemplateEngine()
    posts = [
        Post(
            filename="2024-08-01-hello_world",
            title="Hello World",
            content="Hello world!",
            publish_date=datetime(2024, 8, 1),
        )
    ]

    index = template_engine.generate_index(posts)

    index_page = IndexPage(index)
    assert index_page.heading == "My Blog"

def test_index_shows_posts() -> None:
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
    assert index_page.posts() == [
        {"link": "posts/2024-08-01-hello_world.html", "text": "1 Aug 2024 Hello World"},
        {"link": "posts/2024-08-02-hello_world_again.html", "text": "2 Aug 2024 Hello World again!"},
    ]

def test_index_footer_shows_links() -> None:
    template_engine = TemplateEngine()
    posts = [
        Post(
            filename="2024-08-01-hello_world",
            title="Hello World",
            content="Hello world!",
            publish_date=datetime(2024, 8, 1),
        )
    ]

    index = template_engine.generate_index(posts)

    index_page = IndexPage(index)
    assert index_page.footer() == {"RSS": "/atom.xml", "Mastodon": "https://mastodon.social/@alexjcoleman"}
