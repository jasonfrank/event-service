Gupta Event API Documentation

Updated: 2013-06-20

Quick Start Guide
=================

You can get started right away by following the instructions in
setup.sh to get virtualenv up and running. Then, in bash:

  source setup.sh

This will setup the environment variables and libraries you need.

Edit the file src/gupta/config.py to point to your database server, or
uncomment the SQLite configuration for a quick dev environment.

To run the event server:

  python src/gupta/server.py

Click "Allow" on the security widget that pops up in OS X.

Try out the event service with:

  python src/post_test.py

You should see one passing and one failing post. After that, you can
navigate your browser to:
[http://0.0.0.0:8080/getEvents?applicationId=1&start=0]
You should see the test event.

Prerequisites
=============

You will need MySQL running for the MySQL service, although the
sqlite3 configuration can be uncommented for an easy trial.

Virtualenv eases setting up a fresh environment:

  sudo easy_install pip
  sudo pip install virtualenv

pip is a nice package installer for Python.

Setup
=====

Virtualenv
----------

Create a new virtual environment with:

  virtualenv VIRT

This sets up a new virtual environment named VIRT in the VIRT/ folder.
Activate the environment and get everything setup with:

  source VIRT/bin/activate
  source setup.sh

These two commands need to be run at the beginning of every bash
session.

Packages
--------

The event service depends on:

* MySQL-python
* web.py
* requests

Nose is a testing environment I haven't quite figured out yet.

Python Path
-----------

The PYTHONPATH environment variable needs to be set. setup.sh takes
care of this.

The Database
------------

The db/ folder contains scripts to setup tables in MySQL or SQLite3.

MySQL setup example:

  echo 'create database if not exists gupta_event;' | mysql
  mysql gupta_event < db/mysql_tables.sql

SQLite3 setup example:

  mkdir data
  sqlite3 data/event.db < db/sqlite_tables.sql

Configuration
-------------

Configuration right now is handled in src/gupta/config.py. The only
item to be configured so far is the database. Specify the data source
name and any parameters it needs (filename, username, password,
database name, etc).

The Server
==========

The server can be run with:

  python src/gupta/server.py

It starts up listening on the localhost on port 8080. I haven't done
anything fancy at the OS level with firewalls, just clicked Allow. I
need to test this with remote hosts to make sure it can get through.

Testing
=======

A basic post test can be run with:

  python src/post_test.py

The beginnings of a more comprehensive test suite are run with:

  python src/gupta/eventtest.py

All tests should pass. Testing needs to be more comprehensive.
