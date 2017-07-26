.. _db:

========
Database
========

istSOS architecture permit to use differrent database. Action creators and
retrievers are the specific class packages that should be implemented to support
multi database.

Each database architecture shall be implemented adopting best practice
techniques that enhance a specific database type.

Due to the SOS 2.0 standard approach the tables containing obeserved values are
build on the go. During an *InsertSensor* request a minimal configuration is
stored in the database and only during an *InsertObservation* request the
tables containing the actual observed values are created and the data is
inserted.

Depending on the :ref:`systemtypes` different database configuration are
designed.

Current database implementations:

.. toctree::
    :maxdepth: 2

    db-postgres
