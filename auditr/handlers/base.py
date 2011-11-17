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
    
    def _accepted_mimetypes(self):
        return self.request.headers['accept'].split(',')
    
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



