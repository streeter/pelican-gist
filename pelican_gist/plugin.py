# -*- coding: utf-8 -*-
"""
Gist embedding plugin for Pelican
=================================

This plugin allows you to embed `Gists`_ into your posts.

.. _Gists: https://gist.github.com/

"""
import logging
import os
import re

from jinja2 import Template
from pelican import signals


logger = logging.getLogger(__name__)
gist_regex = re.compile(r'(<p>\[gist:id\=([0-9]+),file\=([^\]]+)\]</p>)')
gist_template = Template("""<div class="gist">
    <script src='{{script_url}}'></script>
    <noscript>
        <pre><code>{{code}}</code></pre>
    </noscript>
</div>""")


def html_output(script_url, code):
    return ""


def gist_url(gist_id, filename):
    return "https://raw.github.com/gist/{}/{}".format(gist_id, filename)


def script_url(gist_id, filename):
    return "https://gist.github.com/{}.js?file={}".format(gist_id, filename)


def get_cache(gist_id, filename):
    return None


def set_cache(gist_id, filename, body):
    pass


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


def replace_gist_tags(generator):
    """Replace gist tags in the article content."""
    should_cache = generator.context.get('GIST_CACHE_ENABLED', True)

    for article in generator.articles:
        for match in gist_regex.findall(article._content):
            gist_id = match[1]
            filename = match[2]
            logger.info('[gist]: found gist id {} and filename {}'.format(
                gist_id,
                filename
            ))

            if should_cache:
                body = get_cache(gist_id, filename)

            # Fetch the gist
            if not body:
                body = fetch_gist(gist_id, filename)

                if should_cache:
                    set_cache(gist_id, filename, body)

            # Create a context to render with
            context = generator.context.copy()
            context.update({
                'script_url': script_url(gist_id, filename),
                'code': body,
            })

            # Render the template
            replacement = gist_template.render(context)

            article._content = article._content.replace(match[0], replacement)


def register():
    """Plugin registration."""

    signals.article_generator_finalized.connect(replace_gist_tags)
