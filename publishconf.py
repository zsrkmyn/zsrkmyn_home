#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://zsrkmyn.github.io'
RELATIVE_URLS = True

FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = False

CC_LICENSE = 'CC-BY-NC-SA'
# Following items are often useful when publishing

DISQUS_SITENAME = "stephens-home"
GOOGLE_ANALYTICS = "UA-102901287-1"

PLUGINS += ['minify']
MINIFY = {
  'remove_comments': True,
  'remove_all_empty_space': True,
  'remove_optional_attribute_quotes': True,
  'keep_pre': True,
  'pre_tags': ['pre', 'code', 'textarea', 'tt'],
}
