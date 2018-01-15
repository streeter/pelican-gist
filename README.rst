Pelican Gist Tag
================

Pelican Gist Tag is a library to make it easy to GitHub Gists in your Pelican_ blogs.

Installation
------------

To install pelican-gist, simply:

.. code-block:: bash

    $ pip install pelican-gist

Then add a bit of code to your blog configuration:

.. code-block:: python

    PLUGINS = [
        # ...
        'pelican_gist',
        # ...
    ]

Usage
-----

In your articles, just add lines to your posts that look like:

.. code-block:: html

    [gist:id=3254906,file=brew-update-notifier.sh]

This will tell the plugin to insert gist id ``3254906`` and choose the file ``brew-update-notifier.sh`` into your post. The resulting HTML will look like:

.. code-block:: html

    <div class="gist">
        <script src='https://gist.github.com/3254906.js?file=brew-update-notifier.sh'></script>
        <noscript>
            <pre><code>#!/bin/bash ...</code></pre>
        </noscript>
    </div>

If your gist has only a single file, you can also specify the gist like so:

.. code-block:: html

    [gist:id=3254906]

Notice it is using the id only. The resulting HTML will look like:

.. code-block:: html

    <div class="gist">
        <script src='https://gist.github.com/3254906.js'></script>
        <noscript>
            <pre><code>#!/bin/bash ...</code></pre>
        </noscript>
    </div>

If a file type is specified, uses pygment to highlight the noscript version of the code:

.. code-block:: html

    [gist:id=3254906,file=brew-update-notifier.sh,filetype=bash]

There is also support for private gists where they have the gist id that looks like ``e34db4c532a6cfa1f711``.

Settings
--------

``GIST_CACHE_ENABLED`` - Specifies whether to cache the gist on disk or not. Default is ``True``. (Optional)
``GIST_PYGMENTS_STYLE`` - Style used by pygments for syntax highlighting. Possible values are the strings from `pygments.styles.get_all_styles()`. Default is ``'default'``. (Optional)
``GIST_PYGMENTS_LINENUM`` - Defines if pygments should add line numbers to the rendered HTML. Default is ``False``. (Optional)

Testing
---------

Install the necessary requirements with `pip install -r requirements.txt`. Once those are installed, you can run the tests with: `py.test`. So the whole workflow looks like:

.. code-block:: bash

    $ pip install -r requrements.txt
    Successfully installed pytest requests mock py
    Cleaning up...
    $ py.test
    ======================== test session starts =========================
    platform darwin -- Python 2.7.6 -- pytest-2.5.1
    collected 5 items

    pelican_gist/test_plugin.py .....

    ====================== 5 passed in 0.11 seconds ======================


Authors
---------

See `contributors`_ on GitHub.


Changelog
---------

- 0.3.4 - Fix regex to support filetype (credit [@andrlik](https://github.com/andrlik))

- 0.3.3 - Support gists with UTF-8 characters

- 0.3.2 - Added universal wheel support

- 0.3.1 - Fixed an issue with Python 3 and fetching gist content

- 0.3.0 - Added Python 3 support


License
-------

Uses the `MIT`_ license.


.. _Pelican: http://blog.getpelican.com/
.. _contributors: https://github.com/streeter/pelican-gist/graphs/contributors
.. _MIT: http://opensource.org/licenses/MIT
