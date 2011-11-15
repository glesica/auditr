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
        query = 'SELECT * FROM computers'
        limits = []
        params = []
    
        computer_names = self.get_arguments('computer_name')
        if computer_names:
            limits.append(
                '(' + ' OR '.join(['computer_name=%s' for c in computer_names]) + ')'
            )
            params.extend(computer_names)
        
        if limits:
            query = query + ' WHERE ' + ' AND '.join(limits)
        
        computers = self.database.query(query, *params)
        
        self.write({
            'status': 'success',
            'computers': [
                computers
            ]
        })
    
    def post(self):
        body_data = json.loads(self.request.body)
        
        computer = self._create_computer(body_data['computer_name'])
        
        self.write({
            'status': 'success',
            'computer': computer
        })



