AUTHOR = 'Alex Coleman'
SITENAME = "Alex Coleman's Blog"
SITEURL = ""

FEED_ATOM = "atom.xml"

DISPLAY_CATEGORIES_ON_MENU = False

PATH = "content"
ARTICLE_URL = ARTICLE_SAVE_AS = '{category}/{date:%Y}-{date:%m}-{date:%d}-{slug}.html'
PAGE_URL = PAGE_SAVE_AS = "{slug}.html"

ARTICLE_TRANSLATION_ID = False

THEME = "custom"

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
)

# DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
