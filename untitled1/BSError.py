#-*- coding: UTF-8 -*-
import urllib2 as u2
from bs4 import BeautifulSoup
import random,time

user_agents=list()
fp = open('./user_agents', 'r')
line  = fp.readline().strip('\n')
while(line):
    user_agents.append(line)
    line = fp.readline().strip('\n')
fp.close()
length = len(user_agents)
index = random.randint(0, length-1)
user_agent = user_agents[index]





def middleBS(tempurl):
        request = u2.Request(tempurl)
        request.add_header('User-agent', user_agent)
        flag=True
        response = u2.urlopen(request,timeout=20)
        while flag:
            parentSoup=response.read()
            if len(parentSoup)>300:
                flag=False
            else:
                response = u2.urlopen(request)
                print "sleep...."
        soup=BeautifulSoup(parentSoup)
        return soup

tempurl1 = "https://www.baidu.com/s?wd=国奥+百度百科"
soup1=middleBS(tempurl1)
tempurl2="http://baike.baidu.com/link?url=Or7dFt3DwYxdW5uP_KWvjmdRKwchiAeuxMRD1etISAnQfSdy-F6VIfM8XGZyl4O_w8WGN82wB6BYfPK_Gy4bT-qzM5Zm-ixRo4DRCpJqlpPMSHKdQ4dxjAbcTt-LkFQiRGz0w07ZYCHKNp403nd-rFM7rvMOgtJzrAd0EkM-oqy"
soup2=middleBS(tempurl2)

#
# request1 = u2.Request(tempurl1)
# request1.add_header('User-agent', user_agent)
# flag=True
# while flag:
#     response1 = u2.urlopen(request1)
#     time.sleep(5)
#     parentSoup1=response1.read()
#     if len(parentSoup1)>1000:
#         flag=False
#     else:
#         print "sleeping 20s..."
#         print parentSoup1
#         time.sleep(10)
#
#
# tempurl2="http://baike.baidu.com/link?url=Or7dFt3DwYxdW5uP_KWvjmdRKwchiAeuxMRD1etISAnQfSdy-F6VIfM8XGZyl4O_w8WGN82wB6BYfPK_Gy4bT-qzM5Zm-ixRo4DRCpJqlpPMSHKdQ4dxjAbcTt-LkFQiRGz0w07ZYCHKNp403nd-rFM7rvMOgtJzrAd0EkM-oqy"
# request2 = u2.Request(tempurl2)
# request2.add_header('User-agent', user_agent)
# flag=True
# while flag:
#     response2 = u2.urlopen(request2)
#     time.sleep(5)
#     parentSoup2=response2.read()
#     if len(parentSoup2)>1000:
#         flag=False
#     else:
#         print "sleeping 20s..."
#         print parentSoup1
# soup2=BeautifulSoup(parentSoup2)


print soup2
