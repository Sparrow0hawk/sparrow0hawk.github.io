from datetime import datetime
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

from blog.post import Post


class Feed:
    def __init__(self, title: str, link: str, author_name: str):
        self.title = title
        self.link = link
        self.author_name = author_name
        self.posts: list[Post] = []

    def add_post(self, post: Post) -> None:
        self.posts.append(post)

    def add_posts(self, *posts: Post) -> None:
        for post in posts:
            self.add_post(post)

    def build(self, now: datetime) -> str:
        feed = self._build_root_elements(now)
        self._build_post_entries(feed)
        ElementTree.indent(feed)
        tree = ElementTree.tostring(feed).decode("utf-8")
        return tree

    def _build_root_elements(self, now: datetime) -> Element:
        feed = Element("feed", attrib={"xmlns": "http://www.w3.org/2005/Atom"})
        SubElement(feed, "title").text = self.title
        SubElement(feed, "id").text = self.link
        SubElement(feed, "link", attrib={"href": self.link, "rel": "alternate"})
        SubElement(feed, "link", attrib={"href": f"{self.link}atom.xml", "rel": "self"})
        SubElement(feed, "updated").text = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        author = SubElement(feed, "author")
        SubElement(author, "name").text = self.author_name
        return feed

    def _build_post_entries(self, feed: Element) -> None:
        for post in self.posts:
            entry = SubElement(feed, "entry")
            SubElement(entry, "title").text = post.title
            SubElement(entry, "id").text = f"{self.link}posts/{post.filename}.html"
            SubElement(entry, "link", attrib={"href": f"{self.link}posts/{post.filename}.html", "rel": "alternate"})
            SubElement(entry, "updated").text = post.publish_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            SubElement(entry, "content", attrib={"type": "html"}).text = post.content
