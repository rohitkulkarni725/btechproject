import urllib.request, urllib.parse, urllib.error
import json
import ssl
import csv

api_key = 'SGHJ1SNKD31PONN9'
serviceurl = 'https://api.thingspeak.com/channels/1163782/feeds.json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    results = input('Enter number of entries to read: ')
    if len(results) < 1: break

    parms = dict()
    if api_key is not False: parms['api_key'] = api_key
    parms['results'] = results
    url = serviceurl + urllib.parse.urlencode(parms)
    print(url)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
        print(js)
    except:
        js = None

    #if not js or 'status' not in js or js['status'] != 'OK':
        #print('==== Failure To Retrieve ====')
        #print(data)
        #continue

    fields = ['Date','Time',js['channel']['field1'],js['channel']['field2'],js['channel']['field3'],js['channel']['field4']]

    n = range(len(js['feeds']))
    rows = list()
    temp = list()
    for i in n:
        temp.clear()
        stmp = js['feeds'][i]['created_at'].split('T')
        for j in [0,1]:
            temp.append(stmp[j])
        temp.append(js['feeds'][i]['field1'])
        temp.append(js['feeds'][i]['field2'])
        temp.append(js['feeds'][i]['field3'])
        temp.append(js['feeds'][i]['field4'])
        rows.append(temp[:])
    
    print(rows)
    # name of csv file  
    filename = "data.csv"
    
    # writing to csv file  
    with open(filename, 'w') as csvfile:
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        
        # writing the fields  
        csvwriter.writerow(fields)  
        
        # writing the data rows  
        csvwriter.writerows(rows)
    print('Excel sheet created')