import json

import tornado.ioloop
import tornado.web
import tornado.database

class AuditHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database

    def get(self, computer_name):
        computer = self._get_computer(computer_name)
        
        # Get the audit results for the given computer.
        installations = self.database.query(
            '''
            SELECT
                a.application_name,
                a.application_version,
                i.audit_date
            FROM installations i 
            INNER JOIN computers c 
                ON i.computer_id = c.computer_id 
            INNER JOIN applications a 
                ON i.application_id = a.application_id 
            WHERE c.computer_name = %s 
                AND i.audit_date = (
                    SELECT MAX(i2.audit_date)
                    FROM installations i2 
                    WHERE i2.computer_id = i.computer_id
                )
            ORDER BY a.application_name;
            ''',
            computer_name
        )
        if not installations:
            #TODO: This should just return an empty result
            self.send_error(404)
        
        result = {
            'computer': computer.computer_name,
            'date': unicode(installations[0].audit_date),
            'applications': [
                {
                    'name': inst.application_name,
                    'version': inst.application_version
                } for inst in installations
            ]
        }
        
        self.write(result)

    def post(self, computer_name):
        computer = self._get_computer(computer_name)
        
        data = json.loads(self.request.body)
        
        for application in data['applications']:
            result = self.database.execute(
                '''
                INSERT INTO applications (
                    application_name, 
                    application_vendor, 
                    application_version
                ) SELECT 
                    %s, 
                    %s, 
                    %s 
                FROM dual WHERE NOT EXISTS (
                    SELECT * 
                    FROM applications 
                    WHERE 
                        application_name=%s AND 
                        application_vendor=%s AND 
                        application_version=%s
                );
                ''',
                application['name'],
                application['vendor'],
                application['version'],
                application['name'],
                application['vendor'],
                application['version']
            )
            print result
    
    def _get_computer(self, computer_name):
        '''
        Get the computer requested. If we didn't get a valid 
        computer name, send a 404 back to the client.
        '''
        computer = self.database.get(
            'SELECT * FROM computers WHERE computer_name = %s;', 
            computer_name
        )
        if computer:
            return computer
        else:
            self.send_error(404)
            

if __name__ == '__main__':
    database = tornado.database.Connection(
        'localhost',
        'auditr',
        user='root',
        password='doofus',
    )

    application = tornado.web.Application([
        (r'/audit/(.*)', AuditHandler, {'database': database}),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
