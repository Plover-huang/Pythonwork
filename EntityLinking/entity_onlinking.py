#-*- coding: UTF-8 -*-]
import json
import urllib2 as u2, urllib
import random,re
import soaplib
from soaplib.core.util.wsgi_wrapper import run_twisted #发布服务
from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase  #所有服务类必须继承该类
from soaplib.core.service import soap  #声明注解
from soaplib.core.model.clazz import Array #声明要使用的类型
from soaplib.core.model.clazz import ClassModel  #若服务返回类，该返回类必须是该类的子类
from soaplib.core.model.primitive import Integer, String
import logging
import sys

prefix = "http://www.baidu.com"

user_agents = list()
baikePrefix="http://baike.baidu.com/"

debug=0

class Extract():
    def __init__(self, keyword,url):
        self.status=-1#-1(none) for entiry not found;0(Polysemants) for list page;1(Polysemant and content) for page with Polysemant;5(content and label and url not Polysemant maybe synonym) for unique page
        length=len(user_agents)
        index = random.randint(0, length-1)
        self.user_agent = user_agents[index]
        self.keyword=keyword
        self.tempurl=""
        self.flag=0#10for first crawl; 1 for the second crawl
        if url is None:
            self.tempurl="http://baike.baidu.com/search/word?word="+urllib.quote(keyword)
        else:
            self.flag=1
            self.tempurl=url
        self.url=""
        self.poly=dict()
        self.content=self.__fetchBaiKeWeb()
        self.poly=self.__fetchPolysemant()
        self.synonym=self.__fetchSynonym()


    def crawlWebContent(self, tempurl):
        if tempurl is None:
            return None
        request = u2.Request(tempurl)
        request.add_header('User-agent', self.user_agent)
        flag=True
        crawlContent=None
        i=0
        while flag:
            try:
                response = u2.urlopen(request,timeout=20)
                crawlContent=response.read()
                flag=False
            except :
                print "connect failed try again..."
                i=i+1
                if i==3:
                    print "connect failed.exit.."
                    return None
        return crawlContent

    def __fetchBaiKeWeb(self):
        #search_url="http://baike.baidu.com/search/word?word="+urllib.quote(self.keyword)
        webpage=self.crawlWebContent(self.tempurl)
        if webpage is None:
            return None
        no_result_re="百度百科尚未收录词条"
        no_result=re.findall(no_result_re,webpage)
        no_exist_re="<p class=\"sorryCont\"><span class=\"sorryTxt\">"
        no_exist=re.findall(no_exist_re,webpage)
        if len(no_result)!=0 or len(no_exist)!=0:
            self.status=-1
            return None
        else:
            list_result_re="<div class=\"para\" label-module=\"para\"><a target=_blank href=\"(.*?)\">.*?：(.*?)</a></div>"
            list_result=re.findall(list_result_re,webpage)
            if len(list_result)!=0:
                for ll in list_result:
                    self.poly[ll[1]]=baikePrefix+ll[0]#获取了多义词
                self.status=0
                return None
            else:
                main_content_re="<div class=\"main-content\">"
                main_content=re.findall(main_content_re,webpage)
                if len(main_content)!=0:
                    self.status=1
                    return webpage
                else:
                    self.status=-1
                    return  None

    def __fetchPolysemant(self):
        if self.content is None or self.flag==1:
            if self.status==0:
                return self.poly
            else:
                return None
        polysemants=re.findall("<li class=\"item\">▪(.*?)</li>",self.content)
        polysemant={}
        if len(polysemants)==0:
            self.url=self.tempurl
            self.status=5
        for pl in polysemants:
            if pl.__contains__("span"):
                text=re.findall("<span class=\"selected\">(.*?)</span>",pl)
                polysemant[text[0]]=self.tempurl
            else:
                text=re.findall("<a title=\"(.*?)\"", pl)
                url=re.findall("<a title=\".*?\" href='(.*?)#viewPageContent'>",pl)
                polysemant[text[0]]=baikePrefix+url[0]
        return polysemant

    def __fetchSynonym(self):
        if self.status!=5:
            return None
        fullname=str()
        # sys_result_re="<span class=\"viewTip-fromTitle\">(.*?)</span>"
        titlere="<dd class=\"lemmaWgt-lemmaTitle-title\">\n<h1 >(.*?)</h1>"
        title=re.findall(titlere,self.content)
        if len(title)!=0 and title[0]!=self.keyword:
            return title[0]
        return fullname
    def getContent(self):
        return self.content
    def getSynonym(self):
        return self.synonym
    def getPolysemant(self):
        return self.poly
    def getLabel(self):
        return self.label
    def getURL(self):
        return self.url
    def getStatus(self):
        return self.status
    def setURL(self,url):
        self.url=url
    def setContent(self,content):
        self.content=content



class EntityLinkWebService(DefinitionBase):
    def __save_content(self,keyword, content):
        return None
    def __save_polysemant(self,keyword, polysemant):
        return None
    def __save_synonym(self,keyword, synonym):
        return None
    def __disambiguation(self,extObject, keyword, keywords):
        content=extObject.getContent()
        target=0
        kk=content.find("<div class=\"main-content\">",0)
        page=content[kk:]
        for kw in keywords:
            if kw!=keyword:
                target=target+str(page).count(kw)
        return target

    @soap(String, _returns=String)
    def entitylinking(self,keywords_input):
        # print keywords_input
        keywords=keywords_input.encode("utf-8").strip().split(" ")
        keywordsURL = []
        keywords_search=[]
        if debug:
            print "-1(none) for entiry not found;\n0(Polysemants) for list page;\n1(Polysemant and content) for page with Polysemant;\n5(content and label and url not Polysemant maybe synonym) for unique page"
        for keyword in keywords:
            if debug:
                print keyword+"\n=============================================================="
            bke = Extract(keyword,url=None)
            status=bke.getStatus()
            if debug:
                print "status:"+str(status)
            if status==-1:
                if debug:
                    print "entity not found"
                keywordsURL.append("")
                keywords_search.append(keyword)
                continue
            elif status==0 or status==1:
                bkePolysemant = bke.getPolysemant()
                tempTarget=0
                tempUrl=""
                tempPl=""
                for (pl,url) in bkePolysemant.items():
                    content=Extract(pl,url)
                    if content.getContent() is None:
                        if debug:
                            print pl+"\t"+url+"<-- not exist"
                        continue
                    target=self.__disambiguation(content, keyword, keywords)
                    if target>=tempTarget:
                        tempTarget=target
                        tempUrl=url
                        tempPl=pl
                    if debug:
                        print pl+"\t"+url
                keywordsURL.append(tempUrl)
                keywords_search.append(tempPl)
            else:
                bkeSynonym=bke.getSynonym()
                if len(bkeSynonym)!=0:
                    print "同义词:"+bkeSynonym
                    keywords_search.append(bkeSynonym)
                else:
                    keywords_search.append(keyword)
                bkeURL=bke.getURL()
                if debug:
                    print "URL:"+bkeURL
                # bkeLable=bke.getLabel()
                # print "Lable: "+' '.join(bkeLable)
                keywordsURL.append(bkeURL)
            if debug:
                print "==============================================================\n\n";
        ll=len(keywords)
        result=list()
        for i in range(ll):
            tempre=list()
            tempdict=dict()
            if debug:
                print keywords[i]+"\t"+keywords_search[i]+"\t"+keywordsURL[i]
            tempre.append(keywords_search[i])
            tempre.append(keywordsURL[i])
            tempdict[keywords[i]]=tempre
            result.append(tempdict)
        result_json=json.dumps(result)
        return result_json

if __name__ == '__main__':
    if len(sys.argv)>=2:
        if sys.argv[1]=="-d":
            global debug
            debug=1
        else:
            print "unknown parameter"
    if debug:
        print "debugging..."
    else:
        print "release"
    user_agents_path = './user_agents'
    fp = open(user_agents_path, 'r')
    line = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()


    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([EntityLinkWebService], 'entitylink')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server("localhost", 1230, wsgi_application)
        print 'soap server starting......'
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"
    except KeyError:
        print "Error: input word not found in vocabulary"






























