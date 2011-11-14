import sys

import tornado.ioloop
import tornado.web
import tornado.database

from handlers.audits import AuditHandler
from handlers.computers import ComputerHandler
            

if __name__ == '__main__':
    debug = ('--debug' in sys.argv) or ('-d' in sys.argv)

    if debug:
        database = tornado.database.Connection(
            'localhost',
            'auditr',
            user='root',
            password='doofus',
        )
    else:
        pass
    
    urls = [
        (r'/audits', AuditHandler, {'database': database}),
        (r'/computers', ComputerHandler, {'database': database}),
    ]

    application = tornado.web.Application(urls, debug=debug)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
