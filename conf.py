# -*- coding: utf-8 -*-

from __future__ import unicode_literals

########################################
# Configuration, please edit
########################################

# Data about this site
BLOG_AUTHOR = u'Martín Gaitán'
BLOG_TITLE = "tin_nqn"
SITE_URL = "http://mgaitan.github.io"
BASE_URL = "http://mgaitan.github.io/"

BLOG_EMAIL = "gaitan@gmail.com"
BLOG_DESCRIPTION = u'>>> me.geek.post()'

# Nikola is multilingual!
#
# Currently supported languages are:
# bg     Bulgarian
# ca     Catalan
# de     German
# el     Greek [NOT gr!]
# en     English
# eo     Esperanto
# es     Spanish
# fa     Persian
# fi     Finnish
# fr     French
# hr     Croatian
# it     Italian
# jp     Japanese
# nl     Dutch
# pt_br  Portuguese (Brasil)
# pl     Polish
# ru     Russian
# sl     Slovenian [NOT sl_si!]
# tr_tr  Turkish (Turkey)
# zh_cn  Chinese (Simplified)
#
# If you want to use Nikola with a non-supported language you have to provide
# a module containing the necessary translations
# (p.e. look at the modules at: ./nikola/data/themes/default/messages/fr.py).
# If a specific post is not translated to a language, then the version
# in the default language will be shown instead.

# What is the default language?
DEFAULT_LANG = "es"

# What other languages do you have?
# The format is {"translationcode" : "path/to/translation" }
# the path will be used as a prefix for the generated pages location
TRANSLATIONS = {
    DEFAULT_LANG: "",
    # Example for another language:
    # "es": "./es",
}

# Links for the sidebar / navigation bar.
# You should provide a key-value pair for each used language.
NAVIGATION_LINKS = {
    DEFAULT_LANG: (
        ('/about.html', u'Sobre mí'),
        ('/charlas.html', u'Charlas'),
        ('/archive.html', 'Archivos'),
        ('/categories/index.html', u'Categorías'),
        ('/rss.xml', u'RSS'),
    ),
}

# Below this point, everything is optional

# While nikola can select a sensible locale for each language,
# sometimes explicit control can come handy.
# In this file we express locales in the string form that
# python's locales will accept in your OS, by example
# "en_US.utf8" in unix-like OS, "English_United States" in Windows.
# LOCALES = dict mapping language --> explicit locale for the languages
# in TRANSLATIONS. You can ommit one or more keys.
# LOCALE_FALLBACK = locale to use when an explicit locale is unavailable
# LOCALE_DEFAULT = locale to use for languages not mentioned in LOCALES; if
# not set the default Nikola mapping is used.

# POSTS and PAGES contains (wildcard, destination, template) tuples.
#
# The wildcard is used to generate a list of reSt source files
# (whatever/thing.txt).
# That fragment must have an associated metadata file (whatever/thing.meta),
# and opcionally translated files (example for spanish, with code "es"):
#     whatever/thing.txt.es and whatever/thing.meta.es
#
# From those files, a set of HTML fragment files will be generated:
# cache/whatever/thing.html (and maybe cache/whatever/thing.html.es)
#
# These files are combinated with the template to produce rendered
# pages, which will be placed at
# output / TRANSLATIONS[lang] / destination / pagename.html
#
# where "pagename" is specified in the metadata file.
#
# if use_in_feed is True, then those posts will be added to the site's
# rss feeds.
#

POSTS = (
    ("posts/*.rst", "posts", "post.tmpl"),
    ("posts/*.txt", "posts", "post.tmpl"),
)
PAGES = (
    ("stories/*.rst", "stories", "story.tmpl"),
    ("stories/*.txt", "stories", "story.tmpl"),
)

# One or more folders containing files to be copied as-is into the output.
# The format is a dictionary of "source" "relative destination".
# Default is:
# FILES_FOLDERS = {'files': '' }
# Which means copy 'files' into 'output'

# A mapping of languages to file-extensions that represent that language.
# Feel free to add or delete extensions to any list, but don't add any new
# compilers unless you write the interface for it yourself.
#
# 'rest' is reStructuredText
# 'markdown' is MarkDown
# 'html' assumes the file is html and just copies it
COMPILERS = {
    "rest": ('.rst', '.txt'),
    "markdown": ('.md', '.mdown', '.markdown'),
    "textile": ('.textile',),
    "txt2tags": ('.t2t',),
    "bbcode": ('.bb',),
    "wiki": ('.wiki',),
    "ipynb": ('.ipynb',),
    "html": ('.html', '.htm'),
    # Pandoc detects the input from the source filename
    # but is disabled by default as it would conflict
    # with many of the others.
    # "pandoc": ('.rst', '.md', '.txt'),
}

# Nikola is multilingual!
#
# Currently supported languages are:
#   English -> en
#   Greek -> gr
#   German -> de
#   French -> fr
#   Russian -> ru
#   Spanish -> es
#   Italian -> it
#
# If you want to use Nikola with a non-supported language you have to provide
# a module containing the necessary translations
# (p.e. look at the modules at: ./nikola/data/themes/default/messages/fr.py).
# If a specific post is not translated to a language, then the version
# in the default language will be shown instead.

# What is the default language?
DEFAULT_LANG = "es"

# What other languages do you have?
# The format is {"translationcode" : "path/to/translation" }
# the path will be used as a prefix for the generated pages location
TRANSLATIONS = {
    DEFAULT_LANG: "",
    #"gr": "./gr",
    #"de": "./de",
    #"fr": "./fr",
    #"ru": "./ru",
    #"en": "./en",
}

# Paths for different autogenerated bits. These are combined with the
# translation paths.

# Final locations are:
# output / TRANSLATION[lang] / TAG_PATH / index.html (list of tags)
# output / TRANSLATION[lang] / TAG_PATH / tag.html (list of posts for a tag)
# output / TRANSLATION[lang] / TAG_PATH / tag.xml (RSS feed for a tag)
TAG_PATH = "categories"

# If TAG_PAGES_ARE_INDEXES is set to True, each tag's page will contain
# the posts themselves. If set to False, it will be just a list of links.
TAG_PAGES_ARE_INDEXES = True

# Final location is output / TRANSLATION[lang] / INDEX_PATH / index-*.html
INDEX_PATH = ""
# Final locations for the archives are:
# output / TRANSLATION[lang] / ARCHIVE_PATH / ARCHIVE_FILENAME
# output / TRANSLATION[lang] / ARCHIVE_PATH / YEAR / index.html
ARCHIVE_PATH = ""
ARCHIVE_FILENAME = "archive.html"
# Final locations are:
# output / TRANSLATION[lang] / RSS_PATH / rss.xml
RSS_PATH = ""

# Slug the Tag URL easier for users to type, special characters are
# often removed or replaced as well.
SLUG_TAG_PATH = True

# A list of redirection tuples, [("foo/from.html", "/bar/to.html")].
#
# A HTML file will be created in output/foo/from.html that redirects
# to the "/bar/to.html" URL. notice that the "from" side MUST be a
# relative URL.
#
# If you don't need any of these, just set to []

REDIRECTIONS = []

# Commands to execute to deploy. Can be anything, for example,
# you may use rsync:
# "rsync -rav output/* joe@my.site:/srv/www/site"
# And then do a backup, or ping pingomatic.
# To do manual deployment, set it to []
DEPLOY_COMMANDS = ["git push --prefix=output origin master"]

# Where the output site should be located
# If you don't use an absolute path, it will be considered as relative
# to the location of conf.py
OUTPUT_FOLDER = 'output'

# where the "cache" of partial generated content should be located
# default: 'cache'
# CACHE_FOLDER = 'cache'

# Filters to apply to the output.
# A directory where the keys are either: a file extensions, or
# a tuple of file extensions.
#
# And the value is a list of commands to be applied in order.
#
# Each command must be either:
#
# A string containing a '%s' which will
# be replaced with a filename. The command *must* produce output
# in place.
#
# Or:
#
# A python callable, which will be called with the filename as
# argument.
#
# By default, there are no filters.
#
# Many filters are shipped with Nikola.  A list is available in the manual:
# <http://getnikola.com/handbook.html#post-processing-filters>
# FILTERS = {
#    ".jpg": ["jpegoptim --strip-all -m75 -v %s"],
# }

##############################################################################
# Image Gallery Options
##############################################################################

# Galleries are folders in galleries/
# Final location of galleries will be output / GALLERY_PATH / gallery_name
GALLERY_PATH = "galleries"
THUMBNAIL_SIZE = 180
MAX_IMAGE_SIZE = 1280
USE_FILENAME_AS_TITLE = True

##############################################################################
# HTML fragments and diverse things that are used by the templates
##############################################################################

# Data about post-per-page indexes
INDEXES_TITLE = ""  # If this is empty, the default is BLOG_TITLE
INDEXES_PAGES = ""  # If this is empty, the default is 'old posts page %d' translated

# Name of the theme to use.
THEME = "custom"

USE_BUNDLES = False
# Show only teasers in the index pages? Defaults to False.
# INDEX_TEASERS = False

# A HTML fragment describing the license, for the sidebar.
# I recomment using the Creative Commons' wizard:
# http://creativecommons.org/choose/
LICENSE = """
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/2.5/ar/">
<img alt="Creative Commons License BY-NC-SA"
style="border-width:0; margin-bottom:12px;"
src="http://i.creativecommons.org/l/by-nc-sa/2.5/ar/88x31.png"></a>"""

# A small copyright notice for the page footer (in HTML)
CONTENT_FOOTER = u'Contents &copy; 2013 Martín Gaitán'

# To use comments, you can choose between different third party comment
# systems, one of "disqus", "livefyre", "intensedebate", "moot",
#                 "googleplus" or "facebook"
COMMENT_SYSTEM = "disqus"
# And you also need to add your COMMENT_SYSTEM_ID which
# depends on what comment system you use. The default is
# "nikolademo" which is a test account for Disqus. More information
# is in the manual.
COMMENT_SYSTEM_ID = "nqnwebs"


SOCIAL_BUTTONS_CODE = ""

# Modify the number of Post per Index Page
# Defaults to 10
# INDEX_DISPLAY_POST_COUNT = 10

# RSS_LINK is a HTML fragment to link the RSS or Atom feeds. If set to None,
# the base.tmpl will use the feed Nikola generates. However, you may want to
# change it for a feedburner feed or something else.
# RSS_LINK = None

# Show only teasers in the RSS feed? Default to True
RSS_TEASERS = False

# A search form to search this site, for the sidebar. You can use a google
# custom search (http://www.google.com/cse/)
# Or a duckduckgo search: https://duckduckgo.com/search_box.html
# This example should work for pretty much any site we generate.
SEARCH_FORM = ""
# This search form is better for the "site" theme where it
# appears on the navigation bar
#SEARCH_FORM = """
#<!-- Custom search -->
#<form method="get" id="search" action="http://duckduckgo.com/" """\
#"""class="navbar-form pull-left">
#<input type="hidden" name="sites" value="%s"/>
#<input type="hidden" name="k8" value="#444444"/>
#<input type="hidden" name="k9" value="#D51920"/>
#<input type="hidden" name="kt" value="h"/>
#<input type="text" name="q" maxlength="255" """\
#"""placeholder="Search&hellip;" class="span2" style="margin-top: 4px;"/>
#<input type="submit" value="DuckDuckGo Search" style="visibility: hidden;" />
#</form>
#<!-- End of custom search -->
#""" % BLOG_URL

# Google analytics or whatever else you use. Added to the bottom of <body>
# in the default template (base.tmpl).
BODY_END = ""

# Put in global_context things you want available on all your templates.
# It can be anything, data, functions, modules, etc.

GLOBAL_CONTEXT = {}
