"""Configuration information for Gupta Event API

Configuration information is read from event.cfg in the project's root
directory.

Classes:
  - EventConfig: wrapper objects for config information.

Convenience functions:
  - get_database: web.py database object from global config
"""

import web
from ConfigParser import ConfigParser

class EventConfig(ConfigParser):
    """Wrapper objects for config information.

    Config file is 'event.cfg' in project root directory by default.

    Throws IOError at point of initialization if it can't read the
    configuration file.

    Example usage:
      config = EventConfig()
      db = config.get_database()
    """

    def __init__(self, config_file='event.cfg'):
        ConfigParser.__init__(self)
        self._config_file = config_file
        self._read_config_file()
        self._db = None

    def get_database(self):
        """Return database object constructed from config"""
        if self._db is None:
            self._build_db()
        return self._db

    def _read_config_file(self):
        with open(self._config_file, 'r') as f:
            self.readfp(f)

    def _build_db(self):
        items = self.items('database')
        
        # build database parameter list
        parms = dict(items)

        # pass parameters through to web.database creator
        self._db = web.database(**parms)

# setup private global configuration
_default_config_file = 'event.cfg'
_default_config = EventConfig()

def get_database():
    """Return web.database object built from global config"""
    return _default_config.get_database()
