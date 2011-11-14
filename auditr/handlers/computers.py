'''
Code that implements the `/computers` API endpoint.
'''

import json

from base import AuditrHandler


class ComputerHandler(AuditrHandler):
    '''
    Handler for `/computers` endpoint.
    '''
    def initialize(self, database):
        self.database = database
    
    def get(self):
        computer_names = self.get_arguments('computer_name')
        self.write({
            'status': 'success',
            'computers': [
                self._get_computer(n) for n in computer_names
            ]
        })
    
    def post(self):
        body_data = json.loads(self.request.body)
        
        computer = self._create_computer(body_data['computer_name'])
        
        self.write({
            'status': 'success',
            'computer': computer
        })



