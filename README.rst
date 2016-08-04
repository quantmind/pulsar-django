Asynchronous Django
=========================

:Badges: |license|  |pyversions| |status| |pypiversion|
:Master CI: |master-build|_ |coverage-master|
:Documentation: https://github.com/quantmind/pulsar-django
:Downloads: http://pypi.python.org/pypi/pulsar-django
:Source: https://github.com/quantmind/pulsar-django
:Keywords: asynchronous, django, wsgi, websocket, redis


The `pulse` module is a django_ application
for running a django web site with pulsar_.
Add it to the list of your ``INSTALLED_APPS``:

.. code:: python

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


Django Chat Example
=======================

This is a web chat application which illustrates how to run a django
site with pulsar and how to include pulsar asynchronous request middleware
into django.

To run::

    python manage.py pulse

If running for the first time, issue the::

    python manage.py syncdb

command and create the super user.


Message and data backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, messages from connected (websocket) clients are synchronised via
the pulsar data store which starts when the django
site starts.

It is possible to specify a different data store via the
``data-store`` option. For example, it is possible
to use redis_ as an alternative data store
by issuing the following start up command::

    python manage.py pulse --data-store redis://127.0.0.1:6379/3



.. _redis: http://redis.io/
.. _django: https://docs.djangoproject.com/en/1.9/ref/applications/
.. _pulsar: https://github.com/quantmind/pulsar
.. _greenlet: https://greenlet.readthedocs.io
.. |master-build| image:: https://travis-ci.org/quantmind/pulsar-django.svg?branch=master
.. _master-build: http://travis-ci.org/quantmind/pulsar-django
.. |coverage-master| image:: https://coveralls.io/repos/github/quantmind/pulsar-django/badge.svg?branch=master
  :target: https://coveralls.io/github/quantmind/pulsar-django?branch=master
.. |pypiversion| image:: https://badge.fury.io/py/pulsar-django.svg
    :target: https://pypi.python.org/pypi/pulsar-django
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/pulsar-django.svg
  :target: https://pypi.python.org/pypi/pulsar-django
.. |license| image:: https://img.shields.io/pypi/l/pulsar-django.svg
  :target: https://pypi.python.org/pypi/pulsar-django
.. |status| image:: https://img.shields.io/pypi/status/pulsar-django.svg
  :target: https://pypi.python.org/pypi/pulsar-django
