import os, csv, json

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/')

requests = []

for fname in os.listdir(DIR):

    name, date_str, log = fname.split('_')
    request = {
        'computer': {
            'name': name
        },
        'date': '-'.join(date_str.split('-')[:3]), # 1 char month/day?
    }
    
    f = open(os.path.join(DIR, fname), 'r')
    csvfile = csv.reader(f, delimiter='\t')
    csvfile.next() # burn header row

    applications = []
    for line in csvfile:
        applications.append({
            'name': line[1],
            'vendor': line[2],
            'version': line[3]
        })
        
    f.close()

    request['applications'] = applications
    requests.append(request)
    
print json.dumps(requests[0])

