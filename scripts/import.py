import os, httplib, json, csv


DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/')

# Headers
headers = {
    'Content-Type': 'application/json'
}

# Establish connection to the test server (localhost:8888)
conn = httplib.HTTPConnection('localhost', 8888)


def post(audit):
    # POST some data
    conn.request('POST', '/audits', json.dumps(audit), headers)
    resp = conn.getresponse()
    return resp.read()


for fname in os.listdir(DIR):

    name, date_str, log = fname.split('_')
    
    f = open(os.path.join(DIR, fname), 'r')
    csvfile = csv.reader(f, delimiter='\t')
    csvfile.next() # burn header row
    
    request = {
        'computer': {
            'computer_name': name
        },
        'audit_date': '-'.join(date_str.split('-')[:3]),
        'applications': [{
            'application_name': line[1].decode('utf8', 'ignore'),
            'application_vendor': line[2].decode('utf8', 'ignore'),
            'application_version': line[3].decode('utf8', 'ignore')
        } for line in csvfile]
    }
        
    f.close()

    print post(request)



