import os, sys, httplib, json, csv


DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/')

# Headers
headers = {
    'Content-Type': 'application/json'
}

# Establish connection to the server
if len(sys.argv) > 1:
    host = sys.argv[1].split(':')[0]
    port = 8888
    if ':' in sys.argv[1]:
        port = int(sys.argv[1].split(':')[1])
conn = httplib.HTTPConnection(host, port)

print 'Submitting data to host %s:%s' % (host, port)


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



