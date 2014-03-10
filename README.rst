===============================
Reddit Autoposter
===============================

A webapp to automatically post Reddit threads daily or weekly.

I am no longer working on autposter as /u/Deimorz's Automoderator has updated to include this functionality_.


Quickstart
----------

::

    git clone https://github.com/Widdershin/autoposter
    cd autoposter
    pip install -r requirements/dev.txt
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``AUTOPOSTER_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commmands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.

.. _functionality: http://www.reddit.com/r/AutoModerator/comments/1z7rlu/now_available_for_testing_wikiconfigurable/
