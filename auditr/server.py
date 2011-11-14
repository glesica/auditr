import tornado.ioloop
import tornado.web
import tornado.database

from handlers.audits import AuditHandler
from handlers.computers import ComputerHandler
            

if __name__ == '__main__':
    database = tornado.database.Connection(
        'localhost',
        'auditr',
        user='root',
        password='doofus',
    )

    application = tornado.web.Application([
        (r'/audits', AuditHandler, {'database': database}),
        (r'/computers', ComputerHandler, {'database': database}),
    ], debug=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
