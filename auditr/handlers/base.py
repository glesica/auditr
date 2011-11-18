'''
Auditr base handlers.
'''

import json

import tornado.web
import tornado.database


class AuditrHandler(tornado.web.RequestHandler):
    '''
    A base handler for the Auditr app.
    '''
    def initialize(self, database):
        self.database = database
        
        self.default_mimetype = 'application/json'
        self.provided_mimetypes = {
            '*': self._return_json,
            'application/json': self._return_json,
            'text/html': self._return_html,
        }
    
    def _accepted_mimetypes(self):
        #TODO: This sucks, fails when quality setting is present
        return self.request.headers['accept'].split(',')
    
    def _return(self, data, template=None, mime=None):
        '''
        Generates an actual response based on `data`, a `dict`. It 
        tries to respect the `Accepts` header sent by the client.
        Alternatively, if `mime` is specified, then the 
        given mimetype will be used without checking.
        '''
        if mime and mime in self.provided_mimetypes:
            mimetype = mime
        else:
            mimetype = self.default_mimetype
            for m in self._accepted_mimetypes():
                if m in self.provided_mimetypes:
                    mimetype = m
        
        self.set_header('Content-Type', mimetype)
        
        return self.provided_mimetypes[mimetype](data, template)
    
    def _return_json(self, data, template=None):
        # It's just so simple!
        self.finish(data)
    
    def _return_html(self, data, template):
        self.render(template, **{'data': data})
    
    #TODO: Refactor these out somehow, shouldn't need them
    
    def _create_application(self, name, vendor, version):
        '''
        Create a single application instance in the database.
        '''
        #TODO: Error handling for when application already exists
        result = self.database.execute(
            '''
            INSERT INTO applications (
                application_name, 
                application_vendor, 
                application_version
            ) VALUES ( 
                %s, 
                %s, 
                %s 
            )
            ''',
            name,
            vendor,
            version
        )
        return result
    
    def _create_computer(self, computer_name):
        '''
        Create a computer.
        '''
        result = self.database.execute(
            '''
            INSERT INTO computers (
                computer_name
            ) VALUES (
                %s
            )
            ''',
            computer_name
        )
        return self._get_computer(computer_name)
    
    def _get_computer(self, computer_name, create=False):
        '''
        Get the computer requested. If we didn't get a valid 
        computer name, send a 400 back to the client since they 
        asked for an invalid computer. Those jerks.
        
        If `create` is `True`, computer's that don't exist will 
        be created, then returned.
        '''
        computer = self.database.get(
            'SELECT * FROM computers WHERE computer_name = %s;', 
            computer_name
        )
        if computer:
            return computer
        else:
            if create:
                return self._create_computer(computer_name)
            else:
                self.send_error(400)



