.. _actions:

=======
Actions
=======

**Actions** can be identified as single processing units, where each action is
specialized in a specific task. For instance the **uoms action retriever** is
able uniquely to load all the Uoms data entities.

istSOS architecture is thought to be modular in terms of data storage.
In facts creational and retrieval actions can be easyly implemented for
different data storage.

Actions are splitted in four cathegories: builders, creators, retrievers and
servers.

********
Builders
********

Builder actions general aim is to parse request inputs (XML, JSON, HTTP
Parameters, etc) and create data or filter entities. For instance the
**sectionsFilter builder action** create the an entity filter that will
be used by the GetCapabilities actions to decide which XML section return as
in the response.

********
Creators
********

The creators actions aim is to store entities into the database.

**********
Retrievers
**********

The retrievers actions aim is to retrieve entities from the database.

*******
Servers
*******

The servers actions can be identified as the engine of istSOS, these actions
are always composite actions that use a combination of builders, creators and
retrievers to execute incoming requests.
