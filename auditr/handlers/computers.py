'''
Code that implements the `/computers` API endpoint.
'''

import json

from base import AuditrHandler


class ComputerHandler(AuditrHandler):
    '''
    Handler for `/computers` endpoint.
    '''
    def get(self):
        query = 'SELECT * FROM computers'
        limits = []
        params = []

        # Filter by computer name
        computer_names = self.get_arguments('computer_name')
        if computer_names:
            limits.append(
                '(' + ' OR '.join(['computer_name=%s' for c in computer_names]) + ')'
            )
            params.extend(computer_names)
        
        if limits:
            query = query + ' WHERE ' + ' AND '.join(limits)
        
        # Figure out limits and where to start then add those 
        # to the query.
        first = self.get_argument('first', '0')
        count = self.get_argument('count', '50')
        query = query + ' LIMIT %s,%s' % (first, count)
        
        # Run the query and write the response
        computers = self.database.query(query, *params)
        
        response = {
            'status': 'success',
            'computers': computers
        }
        
        self._return(response, 'computers.html')
    
    def post(self):
        body_data = json.loads(self.request.body)
        
        computer = self._create_computer(body_data['computer_name'])
        
        self.finish({
            'status': 'success',
            'computer': computer
        })



