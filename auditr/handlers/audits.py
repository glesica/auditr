'''
Code to implement the /audits API endpoint.
'''

import json

from base import AuditrHandler


class AuditHandler(AuditrHandler):
    '''
    Handler for `/audits` endpoint.
    '''
    def initialize(self, database):
        self.database = database

    def get(self):
        query = '''
            SELECT 
                u.audit_id,
                u.audit_date,
                c.computer_name
            FROM audits u
                INNER JOIN computers c ON u.computer_id = c.computer_id
        '''
        
        limits = []
        params = []

        # Filter on computer_name.
        computer_names = self.get_arguments('computer_name')
        if computer_names:
            limits.append(
                '(' + ' OR '.join(['computer_name=%s' for c in computer_names]) + ')'
            )
            params.extend(computer_names)
        
        # Build and run the audits query, this grabs only 
        # audit meta data, we get the actual list of applications 
        # for each audit later.
        if limits:
            query = query + ' WHERE ' + ' AND '.join(limits)
        
        # Figure out limits and where to start then add those 
        # to the query.
        first = self.get_argument('first', '0')
        count = self.get_argument('count', '50')
        query = query + ' LIMIT %s,%s' % (first, count)
        
        # Run the audits query
        audits = self.database.query(query, *params)
        
        # We go the actual audits, build the output and grab the 
        # list of installed applications for each one as we go.
        applications_query = '''
            SELECT
                a.application_name,
                a.application_vendor,
                a.application_version
            FROM installations i
                INNER JOIN applications a 
                    ON i.application_id = a.application_id
            WHERE
                i.audit_id = %s
        '''
        response = {
            'status': 'success',
            'audits': []
        }
        for audit in audits:
            response['audits'].append({
                'computer': {'computer_name': audit.computer_name},
                'audit_date': str(audit.audit_date),
                'audit_id': audit.audit_id,
                'applications': [
                    app for app in self.database.query(
                    applications_query, 
                    audit.audit_id
                    )
                ]
            })
    
        self.finish(response)

    def post(self):
        data = json.loads(self.request.body)
        
        # Get the computer we are working with, create it if 
        # it doesn't already exist
        computer = self._get_computer(
            data['computer']['computer_name'], 
            create=True
        )
        
        # Add a new audit to the database
        audit_id = self.database.execute(
            '''
            INSERT INTO audits (
	            computer_id,
	            audit_date
            ) VALUES (
	            %s,
	            %s
            )
            ;
            ''',
            computer.computer_id,
            data['audit_date']
        )
        
        # Add any new applications (app+version we haven't seen 
        # before) to the DB.
        self.database.executemany_rowcount(
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
            )
            ;
            ''',
            [
                (
                    a['application_name'], 
                    a['application_vendor'], 
                    a['application_version'],
                    a['application_name'], 
                    a['application_vendor'], 
                    a['application_version']
                ) 
                for a in data['applications']
            ]
        )
        
        # All the applications we need exist, so add the 
        # installation records.
        self.database.executemany_rowcount(
            '''
            INSERT INTO installations (
                audit_id,
                application_id
            ) VALUES (
                %s,
                (
                    SELECT a.application_id FROM applications a WHERE 
                        a.application_name=%s AND
                        a.application_vendor=%s AND
                        a.application_version=%s
                )
            )
            ;
            ''',
            [
                (
                    audit_id, 
                    a['application_name'], 
                    a['application_vendor'], 
                    a['application_version']
                ) 
                for a in data['applications']
            ]
        )
            
        self.write({'status': 'success'})
    
    def _get_audits(self, computer_name, latest=1):
        '''
        Get an audit for the computer with name `computer_name`.
        Returns a dict formatted correctly for use in the 
        `write()` method.
        
        TODO: Refactor method to use fewer queries, use buckets for audits
        '''
        computer = self._get_computer(computer_name)
        
        audits = []
        #TODO: Refactor this whole mess...
        audits_data = self.database.query(
            '''
            SELECT
	            u.audit_id,
	            u.audit_date
            FROM
	            audits u
	            INNER JOIN computers c ON u.computer_id = c.computer_id
            WHERE
	            c.computer_name = %s
            ORDER BY
	            u.audit_date DESC
            LIMIT %d
            ;
            ''' % ('%s', latest,),
            computer_name
        )
        if not audits_data:
            return audits
        
        for audit_row in audits_data:
            apps_data = self.database.query(
                '''
                SELECT
	                a.application_name,
	                a.application_vendor,
	                a.application_version
                FROM
	                installations i
	                INNER JOIN applications a ON i.application_id = a.application_id
                WHERE
	                i.audit_id = %s
                ORDER BY a.application_name
                ;
                ''',
                audit_row.audit_id
            )
            
            audits.append({
                'computer': computer,
                'audit_date': str(audit_row.audit_date),
                'audit_id': audit_row.audit_id,
                'applications': [app_row for app_row in apps_data]
            })
            
        return audits



