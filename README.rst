Asynchronous Django
=========================

:Badges: |license|  |pyversions| |status| |pypiversion|
:Master CI: |master-build|_ |coverage-master|
:Documentation: https://github.com/quantmind/pulsar-django
:Downloads: http://pypi.python.org/pypi/pulsar-django
:Source: https://github.com/quantmind/pulsar-django


The `pulse` module is a django_ application
for running a django web site with pulsar_.
Add it to the list of your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'pulse',
        ...
    )

and run the site via the ``pulse`` command::

    python manage.py pulse

Check the django chat example ``djchat`` for a django chat
application served by a multiprocessing pulsar server.

By default, the ``pulse`` command creates a ``Wsgi`` middleware which
runs the django application in a separate thread of execution from the
main event loop.
This is a standard programming pattern when using asyncio with blocking
functions.
To control the number of thread workers in the event loop executor (which
is a pool of threads) one uses the
``thread-workers`` option. For example, the
following command::

    python manage.py pulse -w 4 --thread-workers 20

will run four process based actors, each with
an executor with up to 20 threads.

Greenlets
===============

It is possible to run django in fully asynchronous mode, i.e. without
running the middleware in the event loop executor.
Currently, this is available when using PostgreSql backend
only, and it requires the greenlet_ library.

To run django using greenlet support::

    python manage.py pulse -w 4 --greenlet

By default it will run the django middleware on a pool of 100 greenlets (and
therefore approximately 100 separate database connections per actor). To
adjust this number::

    python manage.py pulse -w 4 --greenlet 200



.. _django: https://docs.djangoproject.com/en/1.9/ref/applications/
.. _pulsar: https://github.com/quantmind/pulsar
.. _greenlet: https://greenlet.readthedocs.io
.. |master-build| image:: https://travis-ci.org/quantmind/pulsar-django.svg?branch=master
.. _master-build: http://travis-ci.org/quantmind/pulsar-django
.. |coverage-master| image:: https://coveralls.io/repos/github/quantmind/pulsar-django/badge.svg?branch=master
  :target: https://coveralls.io/github/quantmind/pulsar-django?branch=master
