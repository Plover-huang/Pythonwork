import urllib2

url='http://www.baidu.com'
reponse = urllib2.Request(url)
html=urllib2.urlopen(reponse)
html=html.read()
print html