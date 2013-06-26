Gupta Event API Documentation

Updated: 2013-06-21

Contents
========

* Quick Start Guide
* Prerequisites
* Setup
  * Virtualenv
  * Packages
  * Python Path
  * The Database
  * Configuration
* The Server
* Testing
* Running in Apache


Quick Start Guide
=================

You can get started right away by following the instructions in
setup.sh to get virtualenv up and running. Then, in bash:

  source setup.sh

This will setup the environment variables and libraries you need.

Edit the file gupta/config.py to point to your database server, or
uncomment the SQLite configuration for a quick dev environment.

To run the event server in the background and log to event_server.log:

  bin/event_server &>event_server.log &

Click "Allow" on the security widget that pops up in OS X.

Try out the event service with:

  bin/test_post

You should see one passing and one failing post. After that, you can
navigate your browser to:
[http://0.0.0.0:8080/getEvents?applicationId=1&start=0]
You should see the test event.

To kill the service:

  fg 1
  <Ctrl-C>


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

From now on two commands need to be run at the beginning of every bash
session:

  # Activate virtual environment
  source VIRT/bin/activate
  # Export environment variables for MySQL and Python
  source env.sh

Packages
--------

The event service depends on:

* MySQL-python
* web.py
* requests

Nose and paste are testing environments I haven't quite figured out
yet.

Python Path
-----------

The PYTHONPATH environment variable needs to be set. env.sh takes care
of this. env.sh is automatically sourced by setup.sh.

The Database
------------

The db/ folder contains scripts to setup tables in MySQL or SQLite3.

MySQL setup example:

  echo 'create database if not exists gupta_event;' | mysql
  mysql gupta_event < db/mysql_tables.sql

SQLite3 setup example:

  mkdir -p data
  sqlite3 data/event.db < db/sqlite_tables.sql

Configuration
-------------

Configuration right now is handled in gupta/config.py. The only item
to be configured so far is the database. Specify the data source name
and any parameters it needs (filename, username, password, database
name, etc).


The Server
==========

The server can be run with:

  bin/event_server

It starts up listening on the localhost on port 8080. I haven't done
anything fancy at the OS level with firewalls, just clicked Allow. I
need to test this with remote hosts to make sure it can get through.


Testing
=======

A basic post test can be run with:

  bin/test_post

The beginnings of a more comprehensive test suite are run with:

  nosetests

Nose is an automatic testing harness for Python that automatically
finds and runs tests defined with Python's built-in unittest library.

All tests should pass. Testing needs to be more comprehensive.


Running in Apache
=================

Apache needs to be configured to run Python. I don't know much about
this aspect. I've come across a lot of acronyms and I don't know
enough to tell the differences, but perhaps you have more experience
in this area.

From my reading I believe the common way to do this is with WSGI:
[https://code.google.com/p/modwsgi/]

I will add more information here as I learn it.
