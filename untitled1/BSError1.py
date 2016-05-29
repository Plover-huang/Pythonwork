#-*- coding: UTF-8 -*-

import urllib2 as u2
from bs4 import BeautifulSoup
import random,time

prefix = "http://www.baidu.com"

user_agents = list()

class Extract:
    fp = open('./user_agents', 'r')
    line = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()

    def __init__(self, keyword):
        length=len(user_agents)
        index = random.randint(0, length-1)
        self.user_agent = user_agents[index]
        self.keyword=keyword
        self.soup=self.__fetchSoup()
        self.polysemant=self.__fetchPolysemant()
        self.synonym=self.__fetchSynonym()
        self.label=self.__fetchLabel()
        self.property=self.__fetchProperty()


    def __middleBS(self, tempurl):
        request = u2.Request(tempurl)
        request.add_header('User-agent', self.user_agent)
        flag=True
        response = u2.urlopen(request,timeout=20)
        parentSoup=None
        while flag:
            parentSoup=response.read()
            if len(parentSoup)>300:
                flag=False
            else:
                response = u2.urlopen(request,timeout=20)
        soupxx=BeautifulSoup(parentSoup)
        return soupxx

    def __fetchSoup(self):
        # tempurl=prefix+"/s?wd=" + self.keyword + "%20百度百科"
        tempurl="http://www.baidu.com/link?url=CK-pOxB26nGYxvmhvj7GCpOo6EcSW2WuSyQFFUl0G3DyPlZzt1-ZyxOWtoE5m9jmTcKKc1pXYPcj7tD3b3-XYdx8c7aNRvvDGhD1EMMPDjHGCuyFhKPmDymm-doj9bnyrihjqwLkTyS3AlZVMNpW4yzDx7b4-aGRm1LC6JzAKZS"
        soupxx=self.__middleBS(tempurl)
        top_result=soupxx.find('div',{'class':"result-op c-container xpath-log"})
        url=top_result.h3.a["href"]
        title=top_result.h3.a.em.text
        if title.encode("utf-8") == self.keyword:
            self.url=url
            soupxx=self.__middleBS(url)
        else:
            soupxx=None
            print "entity not found"
        return soupxx

    def __fetchPolysemant(self):
        polysemant=dict()
        if self.soup==None:
            return None
        polysemants=self.soup.find_all("li",{'class':'item'})
        if len(polysemants)==0:
            print "polysemant not found"
        else:
            for pl in polysemants:
                if pl.span:
                    polysemant[self.keyword+"_"+pl.span.text]=self.url
                else:
                    polysemant[self.keyword+"_"+pl.a.text]=pl.a["href"]
        return polysemant

    def __fetchSynonym(self):
        fullname=str()
        if self.soup==None:
            return None
        synonym=self.soup.find_all('dd',{'class':'lemmaWgt-lemmaTitle-title'})
        if synonym:
            fullname=synonym.h1.text.encode("utf-8")
        else:
            print "synonym not found"
        return fullname

    def __fetchLabel(self):
        labels=list()
        if self.soup==None:
            return None
        Label=self.soup.find_all('dd',{'class':'open-tag-item'})
        for label in Label:
            labels.append(label.span.a.text)
        if len(labels)==0:
            print "label not found"
        return labels

    def __fetchProperty(self):
        if self.soup==None:
            return None
        property={"属性1":"内容","属性2":"内容","属性3":"内容"}
        return property

    def getSoup(self):
        return self.soup
    def getSynonym(self):
        return self.synonym

    def getPolysemant(self):
        return self.polysemant

    def getProperty(self):
        return self.property

    def getLabel(self):
        return self.label
    def getURL(self):
        return self.url

class Synonym:
    def __init__(self,url,fullname):
        self.url=url
        self.fullname=fullname




xx=Extract("国奥")




'''
soup 的类型是beautifulsoup的对象
'''
