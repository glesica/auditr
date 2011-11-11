import httplib, json

# Test data
data = {
    'date': '2011-11-11',
    'applications':[
        {
            'name': 'Microsoft Office 2007',
            'vendor': 'Microsoft, Inc.',
            'version': '12.0.1'
        },
        {
            'name': 'Adobe CS4', 
            'vendor': 'Adobe, Inc.', 
            'version': '9.2.0'
        },
        {
            'name': 'Adobe CS5', 
            'vendor': 'Adobe, Inc.', 
            'version': '10.2.0'
        }
    ]
}

# Headers
headers = {
    'Content-Type': 'application/json'
}

# Establish connection to the test server (localhost:8888)
conn = httplib.HTTPConnection('localhost', 8888)

# POST some data
conn.request('POST', '/audit/computer01', json.dumps(data), headers)

