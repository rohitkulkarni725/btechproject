import urllib.request, urllib.parse, urllib.error
import json
import ssl

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