ecstatic
========

Slightly NIH Flask-based app to serve static content. It tries to capture 80%
of the use-cases that are normally handled by the likes of nginx and Apache,
only much slower =).

Other packages that do similar, but not quite the same things:

* https://pypi.python.org/pypi/Flask-Ecstatic (sorry about the name!)


Configuration
-------------

Ecstatic has a single configuration file whose location is given via an
environment variable "ECSTATIC_EXPORTS". The file is parsed using Python3's
``configparser`` module, with each section being processed from top to bottom.

Whenever a request comes in, a section is checked for whether or not it
matches. If a match is found, no further sections are examined and the
configuration in said section is used to serve the request.

A section matches a request if it

1. Has a ``match`` key with a regular expression that matches the request's
   path or
2. Has a ``root`` section with no match present.

Any other section is ignored.


match-Sections
~~~~~~~~~~~~~~

Any section that contains a ``match``-key must also contain an ``fspath``-key.
If the URL path matches the expression given, ``fspath`` is interpolated as a
format string, with positional arguments from the expression (missing groups
are empty strings instead of ``None``).

The section must still contain a ``root``-entry, also a format string, which is
used to jail paths.


root-Sections
~~~~~~~~~~~~~

Any section containing just a ``root``-entry will simply serve content from the
given root path, mapping 1:1 onto URLs.


Examples
--------

A simple configuration that serves content from users
``public_html``-directories (which are assumed to all be inside ``/home``) and
``/var/www`` otherwise:

.. code-block:: ini

    [homes]
    # exposes /home/bob/public_html/ on http://example.org/~bob/
    match = ^~([a-zA-Z0-9]+)(/.*)?$
    fspath = /home/{0}/public_html{1}
    root = /home/{0}
    dirindex = on

    [www]
    root = /var/www
