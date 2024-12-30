AUTHOR = 'Alex Coleman'
SITENAME = "Alex Coleman's Blog"
SITEURL = "https://www.alexjcoleman.me"

DISPLAY_CATEGORIES_ON_MENU = False

PATH = "content"
ARTICLE_URL = ARTICLE_SAVE_AS = '{category}/{date:%Y}-{date:%m}-{date:%d}-{slug}.html'
PAGE_URL = PAGE_SAVE_AS = "{slug}.html"

DEFAULT_PAGINATION = 20

ARTICLE_TRANSLATION_ID = False

THEME = "custom"

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ATOM = "atom.xml"
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
