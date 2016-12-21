#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Stephen Zhang'
SITENAME = "ASenR's Home"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('email', 'zsrkmyn@gmail.com'),
          ('twitter', 'https://twitter.com/zsrkmyn'),
          ('linkedin', 'https://www.linkedin.com/in/zsrkmyn'),
          ('github', 'https://github.com/zsrkmyn'),)

DEFAULT_PAGINATION = False

THEME = 'pelican-hyde'

PROFILE_IMAGE = 'avatar.jpg'
BIO = 'Lazy...'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
