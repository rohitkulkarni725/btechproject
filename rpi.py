from __future__ import print_function
import http
import urllib
import time
import json
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import time
from RF24 import *
import RPi.GPIO as GPIO

def try_read_data(channel=0):
    radio.startListening()
    if radio.available():
        while radio.available():
            len = radio.getDynamicPayloadSize()
            receive_payload = radio.read(len)
            info = receive_payload.decode('utf-8')
            # First, stop listening so we can talk
            print(receive_payload)
            print('Got response.')
            return info
            # Now, resume listening so we catch the next packets.
            

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rf_adr = list()

while True:
    url = 'https://btechproject.pythonanywhere.com/ota/details'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup('p')
    temp = str(tags[0])
    y = int(temp.split(':')[1].split()[0].split('<')[0])
    print('Number of modules is', y)

    url1 = 'https://btechproject.pythonanywhere.com/rfadr/details'
    html = urlopen(url1, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup('p')
    act = int(str(tags[0]).split(':')[2][1])
    adr = str(tags[0]).split(':')[3][1] + str(tags[0]).split(':')[3][2]

    url2 = 'https://btechproject.pythonanywhere.com/field/details'
    html = urlopen(url2, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup('p')
    m_field = str(tags[0]).split(':')[2].split('<')[0].split()[0]
    t_field = str(tags[0]).split(':')[3].split('<')[0].split()[0]
    h_field = str(tags[0]).split(':')[4].split('<')[0].split()[0]
    li_field = str(tags[0]).split(':')[5].split('<')[0].split()[0]
    st = "field"
    field_no = [(st+m_field),(st+t_field),(st+h_field),(st+li_field)]

    for i in range(len(rf_adr)):
        if rf_adr[i-1] == adr:
            flag = True
        else:
            flag = False

    if act == 1 and not flag:
        rf_adr.append(adr)
    elif act == 0 and flag:
        rf_adr.remove(adr)

    ad = dict()
    max = len(rf_adr) - 1
    if act == 1 and not flag:
        ad[rf_adr[max]] = field_no
    elif act == 0 and flag:
        ad.pop(adr)

    for i in range(rf_adr):
        radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)
        pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
        radio.begin()
        radio.setAutoAck(False);
        radio.enableDynamicPayloads()
        radio.setRetries(5,15)
        radio.printDetails()
        info = try_read_data()
        apikey = 'I66I2LSNS1QBVH1K'
        paramsd = dict()
        #paramsd['field1'] = random.randrange(0,60,1)
        #paramsd['field2'] = random.randrange(0,100,1)
        #paramsd['field3'] = random.randrange(0,100,1)
        #paramsd['field4'] = random.randrange(0,500,1)
        #paramsd['field5'] = random.randrange(0,3000,1)
        paramsd[a[adr][0]] = moisture
        paramsd[a[adr][1]] = temperature
        paramsd[a[adr][2]] = humidity
        paramsd[a[adr][3]] = light_intensity
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