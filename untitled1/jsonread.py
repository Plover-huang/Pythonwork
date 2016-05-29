# coding: utf-8
# import json,time
#
# with open("data_temp.json",'r') as f:
#     rl=f.readline()
#     while rl:
#         kk = json.loads(rl)
#         print kk
#         print "url "+kk["url"][-8:]
#         print "topic "+kk["topic"]
#         print "title "+kk["title"]
#         print "desc "+kk["desc"]
#         rl=f.readline()
#         time.sleep(10000)

from bs4 import BeautifulSoup
import urllib2
content=u"艺术"
content = content.encode('utf-8')
content = urllib2.quote(content)
url="https://www.zhihu.com/topics#%s" % content
print url
html = urllib2.urlopen(url)
html = html.read()
soup = BeautifulSoup(html,"html.parser")
topics = soup.find_all('div',{"class":"item"})
topics_even = soup.find_all('div',{"class":'item even'})
topics+=topics_even
data={}
questions=[]
print "all sub topics are:"
for t in topics:
    print "    "+t.div.a.img.strong.text
