import tornado.ioloop
import tornado.web
import tornado.database

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database

    def get(self, computer_name):
        query = 'SELECT * FROM computers WHERE computer_name=%s;'
        computer = self.database.get(query, computer_name)
        if computer:
            self.write(computer)
        else:
            self.send_error(404)

    def put(self):
        pass

if __name__ == '__main__':
    database = tornado.database.Connection(
        'localhost',
        'auditr',
        user='root',
        password='doofus',
    )

    application = tornado.web.Application([
        (r'/computer/(.*)', MainHandler, {'database': database}),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
