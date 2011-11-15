import sys, logging

import tornado.ioloop
import tornado.web
import tornado.database

import handlers
from config import *
            

if __name__ == '__main__':
    debug = ('--debug' in sys.argv) or ('-d' in sys.argv)

    # Set up logging
    log_format = '%(asctime)s %(levelname)s (%(filename)s):%(message)s'
    
    if debug:
        logging.basicConfig(
            format=log_format, 
            level=logging.DEBUG
        )
    else:
        logging.basicConfig(
            filename=LOG_FILE, 
            format=log_format, 
            level=logging.WARNING
        )

    logging.info('Connecting to database: %s' % DATABASE_HOST)

    # Configure the database
    database = tornado.database.Connection(
        DATABASE_HOST,
        DATABASE_NAME,
        DATABASE_USER,
        DATABASE_PASSWORD,
    )

    # Configure URLs
    urls = [
        (r'/audits', handlers.AuditHandler, {'database': database}),
        (r'/computers', handlers.ComputerHandler, {'database': database}),
    ]

    logging.info('Starting server on port %s' % SERVER_PORT)

    application = tornado.web.Application(urls, debug=debug)
    application.listen(SERVER_PORT)
    tornado.ioloop.IOLoop.instance().start()



