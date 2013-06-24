"""Configuration information for Gupta Event API"""

import web

# MySQL database connection
# host='<hostname>' and port=<port_no> are optional parameters
# db = web.database(dbn='mysql', db='gupta_event',
#                   user='gupta', pw='draft1044')

# SQLite database connection
db = web.database(dbn='sqlite', db='data/event.db')
