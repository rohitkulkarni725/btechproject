from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://btechproject.pythonanywhere.com/ota/details'
html = urlopen(url, context=ctx).read()
#print(html)
soup = BeautifulSoup(html, "html.parser")
#print(soup)

tags = soup('p')
#print(tags)
temp = str(tags[0])
#print(temp)
y = int(temp.split(':')[1].split()[0].split('<')[0])
#x = y[1].split()
#z = x[0].split('<')
#w = int(z[0])
print('Number of modules is', y)

url1 = 'https://btechproject.pythonanywhere.com/rfadr/details'
html = urlopen(url1, context=ctx).read()
#print(html)
soup = BeautifulSoup(html, "html.parser")
#print(soup)

tags = soup('p')
#print(tags)
act = int(str(tags[0]).split(':')[2][1])
print(act)
adr = str(tags[0]).split(':')[3][1] + str(tags[0]).split(':')[3][2]
print(adr)

url2 = 'https://btechproject.pythonanywhere.com/field/details'
html = urlopen(url2, context=ctx).read()
#print(html)
soup = BeautifulSoup(html, "html.parser")
#print(soup)

tags = soup('p')
#print(tags)
#print(str(tags[0]).split(':'))
#print(int(str(tags[0]).split(':')[3].split('<')[0].split()[0]))
m_field = int(str(tags[0]).split(':')[2].split('<')[0].split()[0])
t_field = int(str(tags[0]).split(':')[3].split('<')[0].split()[0])
h_field = int(str(tags[0]).split(':')[4].split('<')[0].split()[0])
li_field = int(str(tags[0]).split(':')[5].split('<')[0].split()[0])
print(m_field)
print(t_field)
print(h_field)
print(li_field)