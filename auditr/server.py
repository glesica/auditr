import sys, logging

import tornado.ioloop
import tornado.web
import tornado.database
from tornado.options import define, options

import handlers
from config import *


define('dbhost', default='localhost:3306', help='Database host', type=str)
define('debug', default=False, help='Debugging mode', type=bool)
define('port', default=8888, help='Port to run on', type=int)


def main():
    tornado.options.parse_command_line()
    
    # Set up logging
    log_format = '%(asctime)s %(levelname)s (%(filename)s):%(message)s'
    
    if options.debug:
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
    
    logging.info('Starting server on port %s' % SERVER_PORT)
    
    database = tornado.database.Connection(
        DATABASE_HOST,
        DATABASE_NAME,
        DATABASE_USER,
        DATABASE_PASSWORD,
    )
    urls = [
        (r'/audits', handlers.AuditHandler, {'database': database}),
        (r'/computers', handlers.ComputerHandler, {'database': database}),
    ]
    
    app = tornado.web.Application(
        urls, 
        debug=options.debug,
        template_path='auditr/templates/',
        static_path='auditr/static/',
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()



