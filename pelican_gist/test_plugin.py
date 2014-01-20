# -*- coding: utf-8 -*-
"""
Test pelican-gist
=================

Test stuff in pelican_gist.

"""
from __future__ import unicode_literals
import os

from pelican_gist import plugin as gistplugin
from mock import patch
import requests.models


def test_gist_url():
    gist_id = str(3254906)
    filename = 'brew-update-notifier.sh'

    # Test without a filename
    url = gistplugin.gist_url(gist_id)
    assert gist_id in url

    # Test with filename
    url = gistplugin.gist_url(gist_id, filename)
    assert url.endswith(filename)
    assert gist_id in url


def test_script_url():
    gist_id = str(3254906)
    filename = 'brew-update-notifier.sh'

    # Test without a filename
    url = gistplugin.script_url(gist_id)
    assert url.endswith('.js')
    assert gist_id in url

    # Test with filename
    url = gistplugin.script_url(gist_id, filename)
    assert url.endswith(filename)
    assert 'file={}'.format(filename) in url
    assert gist_id in url


def test_cache_filename():
    path_base = '/tmp'
    gist_id = str(3254906)
    filename = 'brew-update-notifier.sh'

    # Test without a filename
    path = gistplugin.cache_filename(path_base, gist_id)
    assert path.startswith(path_base)
    assert path.endswith('.cache')

    # Test with filename
    path = gistplugin.cache_filename(path_base, gist_id, filename)
    assert path.startswith(path_base)
    assert path.endswith('.cache')


def test_set_get_cache():
    path_base = '/tmp'
    gist_id = str(3254906)
    filename = 'brew-update-notifier.sh'
    body = """Some gist body"""

    # Make sure there is no cache
    for f in (gistplugin.cache_filename(path_base, gist_id),
              gistplugin.cache_filename(path_base, gist_id, filename)):
        if os.path.exists(f):
            os.remove(f)

    # Get an empty cache
    cache_file = gistplugin.get_cache(path_base, gist_id)
    assert cache_file is None

    cache_file = gistplugin.get_cache(path_base, gist_id, filename)
    assert cache_file is None

    # Set a cache file
    gistplugin.set_cache(path_base, gist_id, body)

    # Fetch the same file
    cached = gistplugin.get_cache(path_base, gist_id)
    assert cached == body

    # Set a cache file
    gistplugin.set_cache(path_base, gist_id, body, filename)

    # Fetch the same file
    cached = gistplugin.get_cache(path_base, gist_id, filename)
    assert cached == body


def test_fetch_gist():
    """Ensure fetch_gist returns the response content as a string."""
    CODE_BODY = "code"
    with patch('requests.get') as get:
        return_response = requests.models.Response()
        return_response.status_code = 200
        return_response._content= CODE_BODY.encode()
        get.return_value = return_response
        assert gistplugin.fetch_gist(1) == CODE_BODY
