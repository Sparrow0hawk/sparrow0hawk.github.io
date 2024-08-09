from datetime import datetime

from blog.feed import Feed
from blog.post import Post


def test_build() -> None:
    feed = Feed(title="Hello blog", link="https://hello.blog", author_name="John Smith")
    post = Post(filename="2024-08-01-hello_world", title="Hello World", content="Hello world!", publish_date=datetime(2024, 8, 1))
    feed.add_post(post)

    feed_output = feed.build(now=datetime(2020, 1, 1, 12))

    assert feed_output == """<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Hello blog</title>
  <link href="https://hello.blog" />
  <updated>2020-01-01T12:00:00Z</updated>
  <author>
    <name>John Smith</name>
  </author>
  <entry>
    <title>Hello World</title>
    <id>https://hello.blog/posts/2024-08-01-hello_world.html</id>
    <updated>2024-08-01T00:00:00Z</updated>
  </entry>
</feed>"""


def test_add_post() -> None:
    feed = Feed(title="Hello blog", link="https://hello.blog", author_name="John Smith")
    post = Post(filename="2024-08-01-hello_world", title="Hello World", content="Hello world!", publish_date=datetime(2024, 8, 1))

    feed.add_post(post)

    assert feed.posts == [post]


def test_add_posts() -> None:
    feed = Feed(title="Hello blog", link="https://hello.blog", author_name="John Smith")
    post1 = Post(filename="2024-08-01-hello_world", title="Hello World", content="Hello world!", publish_date=datetime(2024, 8, 1))
    post2 = Post(filename="2024-08-02-hello_world2", title="Hello World2", content="Hello world again!", publish_date=datetime(2024, 8, 2))

    feed.add_posts(post1, post2)

    assert feed.posts == [post1, post2]
