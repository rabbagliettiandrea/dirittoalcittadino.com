# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = 'Avv. Rabbaglietti'
SITENAME = 'Diritto Al Cittadino'

SITEURL = 'http://www.dirittoalcittadino.com'

THEME = 'themes/dirittoalcittadino'

TIMEZONE = 'Europe/Rome'
DEFAULT_LANG = 'it'

PATH = 'content'
PAGE_DIR = 'pages'
ARTICLE_DIR = 'posts'

DEFAULT_CATEGORY = 'Consulenze'

DELETE_OUTPUT_DIRECTORY = True
FILES_TO_COPY = (
    ('../.gitignore', '.gitignore'),
    ('extra/CNAME', 'CNAME'),
)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DISQUS_SITENAME = 'dirittoalcittadino'
GOOGLE_ANALYTICS = 'UA-30293095-1'

DEFAULT_DATE_FORMAT = '%A %d %B %Y'

# Url formation
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

PAGE_URL = 'pagine/{slug}/'
PAGE_SAVE_AS = 'pagine/{slug}/index.html'

CATEGORY_URL = 'articoli/{slug}/'
CATEGORY_SAVE_AS = 'articoli/{slug}/index.html'

TAG_URL = 'tags/{slug}/'
TAG_SAVE_AS = 'tags/{slug}/index.html'