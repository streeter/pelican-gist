# -*- coding: utf-8 -*-
"""
Gist embedding plugin for Pelican
=================================

This plugin allows you to embed `Gists`_ into your posts.

.. _Gists: https://gist.github.com/

"""
import logging
import hashlib
import os
import re


logger = logging.getLogger(__name__)
gist_regex = re.compile(r'(<p>\[gist:id\=([0-9]+),file\=([^\]]+)\]</p>)')
gist_template = """<div class="gist">
    <script src='{{script_url}}'></script>
    <noscript>
        <pre><code>{{code}}</code></pre>
    </noscript>
</div>"""


def html_output(script_url, code):
    return ""


def gist_url(gist_id, filename):
    return "https://raw.github.com/gist/{}/{}".format(gist_id, filename)


def script_url(gist_id, filename):
    return "https://gist.github.com/{}.js?file={}".format(gist_id, filename)


def cache_filename(base, gist_id, filename):
    h = hashlib.md5()
    h.update(gist_id)
    h.update(filename)
    return os.path.join(base, '{}.cache'.format(h.hexdigest()))


def get_cache(base, gist_id, filename):
    cache_file = cache_filename(base, gist_id, filename)
    if not os.path.exists(cache_file):
        return None
    with open(cache_file, 'r') as f:
        return f.read()


def set_cache(base, gist_id, filename, body):
    with open(cache_filename(base, gist_id, filename), 'w') as f:
        f.write(body)


def fetch_gist(gist_id, filename):
    """Fetch a gist and return the raw contents."""
    import requests

    url = gist_url(gist_id, filename)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Got a bad status looking up gist.')
    body = response.content
    if not body:
        raise Exception('Unable to get the gist content.')

    return body


def setup_gist(pelican):
    """Setup the default settings."""

    pelican.settings.setdefault('GIST_CACHE_ENABLED', True)
    pelican.settings.setdefault('GIST_CACHE_LOCATION',
        '/tmp/gist-cache')

    # Make sure the gist cache directory exists
    cache_base = pelican.settings.get('GIST_CACHE_LOCATION')
    if not os.path.exists(cache_base):
        os.makedirs(cache_base)


def replace_gist_tags(generator):
    """Replace gist tags in the article content."""
    from jinja2 import Template
    template = Template(gist_template)

    should_cache = generator.context.get('GIST_CACHE_ENABLED')
    cache_location = generator.context.get('GIST_CACHE_LOCATION')

    for article in generator.articles:
        for match in gist_regex.findall(article._content):
            gist_id = match[1]
            filename = match[2]
            logger.info('[gist]: Found gist id {} and filename {}'.format(
                gist_id,
                filename
            ))

            if should_cache:
                body = get_cache(cache_location, gist_id, filename)

            # Fetch the gist
            if not body:
                logger.info('[gist]:   Gist did not exist in cache, fetching...')
                body = fetch_gist(gist_id, filename)

                if should_cache:
                    logger.info('[gist]:   Saving gist to cache...')
                    set_cache(cache_location, gist_id, filename, body)
            else:
                logger.info('[gist]:   Found gist in cache.')

            # Create a context to render with
            context = generator.context.copy()
            context.update({
                'script_url': script_url(gist_id, filename),
                'code': body,
            })

            # Render the template
            replacement = template.render(context)

            article._content = article._content.replace(match[0], replacement)


def register():
    """Plugin registration."""
    from pelican import signals

    signals.initialized.connect(setup_gist)

    signals.article_generator_finalized.connect(replace_gist_tags)
