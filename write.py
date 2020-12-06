import http
import urllib
import time
import json
import random

apikey = 'I66I2LSNS1QBVH1K'
while True:
    paramsd = dict()
    paramsd['api_key'] = apikey
    paramsd['field1'] = random.randrange(0,60,1)
    paramsd['field2'] = random.randrange(0,100,1)
    paramsd['field3'] = random.randrange(0,100,1)
    paramsd['field4'] = random.randrange(0,500,1)
    params = urllib.parse.urlencode(paramsd)
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(response)
        conn.close()
    except:
        print("connection failed")
        break