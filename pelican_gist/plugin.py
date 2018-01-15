# -*- coding: utf-8 -*-
"""
Gist embedding plugin for Pelican
=================================

This plugin allows you to embed `Gists`_ into your posts.

.. _Gists: https://gist.github.com/

"""
from __future__ import unicode_literals
import hashlib
import logging
import os
import re
import codecs
import pygments

logger = logging.getLogger(__name__)
gist_regex = re.compile(
    r'(<p>\[gist:id\=([0-9a-fA-F]+)(,file\=([^\],]+))?(,filetype\=([a-zA-Z]+))?\]</p>)')
gist_template = """<div class="gist">
    <script src='{{script_url}}'></script>
    <noscript>
        {{code}}
    </noscript>
</div>"""

def gist_url(gist_id, filename=None):
    url = "https://gist.githubusercontent.com/raw/{}".format(gist_id)
    if filename is not None:
        url += "/{}".format(filename)
    return url


def script_url(gist_id, filename=None):
    url = "https://gist.github.com/{}.js".format(gist_id)
    if filename is not None:
        url += "?file={}".format(filename)
    return url


def cache_filename(base, gist_id, filename=None):
    h = hashlib.md5()
    h.update(str(gist_id).encode())
    if filename is not None:
        h.update(filename.encode())
    return os.path.join(base, '{}.cache'.format(h.hexdigest()))


def get_cache(base, gist_id, filename=None):
    cache_file = cache_filename(base, gist_id, filename)
    if not os.path.exists(cache_file):
        return None
    with codecs.open(cache_file, 'rb', 'utf-8') as f:
        return f.read()


def set_cache(base, gist_id, body, filename=None):
    with codecs.open(cache_filename(base, gist_id, filename), 'wb', 'utf-8') as f:
        f.write(body)


def fetch_gist(gist_id, filename=None):
    """Fetch a gist and return the contents as a string."""
    import requests

    url = gist_url(gist_id, filename)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Got a bad status looking up gist.')
    body = response.text
    if not body:
        raise Exception('Unable to get the gist contents.')

    return body


def setup_gist(pelican):
    """Setup the default settings."""
    pelican.settings.setdefault('GIST_CACHE_ENABLED', True)
    pelican.settings.setdefault('GIST_CACHE_LOCATION',
                                '/tmp/gist-cache')
    pelican.settings.setdefault('GIST_PYGMENTS_STYLE', 'default')
    pelican.settings.setdefault('GIST_PYGMENTS_LINENUM', False)

    # Make sure the gist cache directory exists
    cache_base = pelican.settings.get('GIST_CACHE_LOCATION')
    if not os.path.exists(cache_base):
        os.makedirs(cache_base)


def render_code(code, filetype, pygments_style):
    """Renders a piece of code into HTML. Highlights syntax if filetype is specfied"""
    if filetype:
        lexer = pygments.lexers.get_lexer_by_name(filetype)
        formatter = pygments.formatters.HtmlFormatter(style=pygments_style)
        return pygments.highlight(code, lexer, formatter)
    else:
        return "<pre><code>{}</code></pre>".format(code)

def replace_gist_tags(generator):
    """Replace gist tags in the article content."""
    from jinja2 import Template
    template = Template(gist_template)

    should_cache = generator.context.get('GIST_CACHE_ENABLED')
    cache_location = generator.context.get('GIST_CACHE_LOCATION')
    pygments_style = generator.context.get('GIST_PYGMENTS_STYLE')
    
    body = None

    for article in generator.articles:
        for match in gist_regex.findall(article._content):
            gist_id = match[1]
            filename = None
            filetype = None
            if match[3]:
                filename = match[3]
            if match[5]:
                filetype = match[5]
            logger.info('[gist]: Found gist id {} with filename {} and filetype {}'.format(
                gist_id,
                filename,
                filetype,
            ))

            if should_cache:
                body = get_cache(cache_location, gist_id, filename)

            # Fetch the gist
            if not body:
                logger.info('[gist]: Gist did not exist in cache, fetching...')
                body = fetch_gist(gist_id, filename)

                if should_cache:
                    logger.info('[gist]: Saving gist to cache...')
                    set_cache(cache_location, gist_id, body, filename)
            else:
                logger.info('[gist]: Found gist in cache.')

            # Create a context to render with
            context = generator.context.copy()
            context.update({
                'script_url': script_url(gist_id, filename),
                'code': render_code(body, filetype, pygments_style)
            })

            # Render the template
            replacement = template.render(context)

            article._content = article._content.replace(match[0], replacement)


def register():
    """Plugin registration."""
    from pelican import signals

    signals.initialized.connect(setup_gist)

    signals.article_generator_finalized.connect(replace_gist_tags)
