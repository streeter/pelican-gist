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

There is also support for private gists where they have the gist id that looks like ``e34db4c532a6cfa1f711``.

Settings
--------

``GIST_CACHE_ENABLED`` - Specifies whether to cache the gist on disk or not. Default is ``True``. (Optional)

License
-------

Uses the `MIT`_ license.


.. _Pelican: http://blog.getpelican.com/
.. _MIT: http://opensource.org/licenses/MIT
