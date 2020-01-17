Installation
============

Requirements
------------

``python-mobilitydb`` has several dependencies beyond an installation of Python 3.x:

* `psycopg2 <http://initd.org/psycopg/docs/>`_ or `asyncpg <https://magicstack.github.io/asyncpg/>`_ to connect to PostgreSQL,
* `postgis <https://github.com/tilery/python-postgis>`_ to connect to PostGIS,
* `Spans <https://spans.readthedocs.io/>`_ for an implementation of PostgreSQL’s range types,
* `python-dateutil <http://labix.org/python-dateutil>`_ for extensions to the standard datetime module,
* `parsec <https://pythonhosted.org/parsec/>`_ for parsing.

Python Package Index
--------------------

``python-mobilitydb`` may be installed from PyPI.

.. code-block:: console

   $ pip install python-mobilitydb


Source
------

The package sources are available at https://github.com/ULB-CoDE-WIT/python-mobilitydb. Building and installing ``python-mobilitydb`` from source can be done with `setuptools <https://setuptools.readthedocs.io/en/latest/>`_:

.. code-block:: console

    $ python setup.py install

Tests
~~~~~

Tests require `pytest <https://docs.pytest.org/en/latest/>`_ and `pytest-asyncio <https://github.com/pytest-dev/pytest-asyncio>`_. 

.. code-block:: console

    $ pytest

The PostgreSQL database server must be started before launching the tests.

Documentation
~~~~~~~~~~~~~

Building the documentation from source requires `Sphinx <http://www.sphinx-doc.org/>`_. By default, the documentation will be rendered in HTML:

.. code-block:: console

    $ python setup.py build_sphinx

For other documentation output formats, see the options in the ``docs`` subdirectory:

.. code-block:: console

    $ cd docs
    $ make
