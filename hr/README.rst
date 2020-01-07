hr
==

hr for human resources: package to update users on a server based on an “inventory” JSON file

Preparing for Development
-------------------------

1. Ensure ``pip`` and ``pipenv`` are installed.
2. Clone repository and enter folder
3. Fetch development dependencies ``make install``
4. Activate virtualenv: ``pipenv shell``

Usage
-----

Make users of host match the contents of provided file:

::

    $ sudo hr users_to_import.json

Export host users in json formatted file:

::

    $ sudo hr --export exported_users.json


Running Tests
-------------

Run tests locally using ``make`` if virtualenv is active:

::

    $ make

If virtualenv isn’t active then use:

::

    $ pipenv run make
