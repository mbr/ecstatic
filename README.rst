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

Any other section is ignored for matching paths.


match-Sections
~~~~~~~~~~~~~~

Any section that contains a ``match``-key must also contain an ``fspath``-key.
If the URL path matches the expression given, ``fspath`` is substituted for it.

The section must still contain a ``root``-entry, which is used to jail paths.


root-Sections
~~~~~~~~~~~~~

Any section containing just a ``root``-entry will simply serve content from the
given root path, mapping 1:1 onto URLs.


Examples
--------

A simple configuration that serves content from users
``public_html``-directories (which are assumed to all be in ``/home``) and
``/var/www`` otherwise:

.. code-block:: ini

    [homes]
    match = ^~([a-zA-Z0-9]+)/public_html((?:/.+)?)$
    fspath = /home/\1/public_html\2
    root = /home
    dirindex = on

    [www]
    root = /var/www
