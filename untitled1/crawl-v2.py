# coding: utf-8

from bs4 import BeautifulSoup
import urllib2 as u2
import json, re,time

import gzip, StringIO,random,types

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

i=0
base_link="http://www.zhihu.com"
N=30
Scon = 1

user_agents = list()



def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def getHTML(url):
    # print "opening %s" % url
    request = u2.Request(url)
    length = len(user_agents)
    index = random.randint(0, length-1)
    user_agent = user_agents[index]
    request.add_header('User-agent', user_agent)
    request.add_header('connection','keep-alive')
    response = u2.urlopen(request)
    html = response.read()
    return html


def parseDebugHTML(html):
    soup=BeautifulSoup(html,"html.parser")
    content = soup.find_all("div",id="zh-question-detail")
    #print content[0]
    textarea = re.findall(r"<textarea class=\"content hidden\">",str(content[0]))

    if textarea:
        con = content[0].textarea.text
        con = con.encode('UTF-8')
        con = str(con)
        con = re.sub(r"[\u4e00-\u9fa5]","",con)
        con = re.sub(r'\w','',con)
        con = re.sub('[,./;\'\":?><=-_+-|)(*&^$#@! ]','',con)
        return  con
    else:
        return content[0].text

def getDesc(html):
    soup=BeautifulSoup(html,"html.parser")
    content = soup.find_all("div",id="zh-question-detail")
    textarea = re.findall(r"<textarea class=\"content hidden\">",str(content[0]))
    if textarea:
        con = content[0].textarea.text
    else:
        con = content[0].text
    con = con.encode('UTF-8')
    con = str(con)
    con = re.sub(r'\w','',con)
    con = re.sub('[,./;\'\":?><=-_+-|)(*&^$#@!\t\n%]','',con)
    return con

def getQuesetion(html):
    soup=BeautifulSoup(html,"html.parser")
    questions = soup.find_all('a',{"class":"question_link"})
    return questions

def getMainTopics(html):
    soup = BeautifulSoup(html,"html.parser")
    content = soup.find_all("a",href=re.compile("#.*"))
    mt=[]
    for c in content:
        mt.append(c.text)
    return mt

def getSubTopics(html,f):
    soup = BeautifulSoup(html,"html.parser")
    topics = soup.find_all('div',{"class":"item"})
    topics_even = soup.find_all('div',{"class":'item even'})
    topics+=topics_even
    data={}
    questions=[]
    print "all sub topics are:"
    for t in topics:
        print "    "+t.div.a.img.strong.text
    for tindex,topic in enumerate(topics):
        # if Scon:
        #     if tindex<19:
        #         continue
        topic_name = topic.div.a.img.strong.text #topic name
        print "processing sub topic "+topic_name
        base_url=base_link+topic.div.a["href"]+"/top-answers?page="
        print base_url[:-6]
        for i in range(1,N+1):
            url=base_url+str(i)
            try:
                questions += getQuesetion(getHTML(url))
            except u2.HTTPError:
                print "404: break at " + url
                break
        len_questions=len(questions)
        print "there are %d questions" % len_questions

        for qindex,question in enumerate(questions): #question for each topic
            sys.stdout.write("processing..."+str(qindex)+"/"+str(len_questions))
            sys.stdout.flush()
            restart_line()
            data["topic"]=topic_name
            question_title = question.text #title
            question_title = re.sub('[,./;\'\":?><=-_+-|)(*&^$#@!\t\n%]','',question_title)
            url = base_link+question["href"]
            try:
                question_desc = getDesc(getHTML(url)).strip() #desc
            except u2.HTTPError:
                print "403: break at "+url
                sleeptime =  random.randint(30, 60)
                time.sleep(sleeptime)
            if question_desc=="":
                question_desc="None"
            data["url"]=url
            data["title"]=question_title
            data["desc"]=question_desc
            cc="{\"url\":\"%s\",\"topic\":\"%s\",\"title\":\"%s\",\"desc\":\"%s\"}\n" % (data["url"],data["topic"],data["title"],data["desc"])
            f.write(cc)
            data={}
        # print "10000 seconds"
        # time.sleep(10000)
        questions=[]
    # global Scon
    # Scon=0

def load_user_agent():
    fp = open('./user_agents', 'r')

    line  = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()


if __name__=="__main__":
    if i:
        url ="http://www.zhihu.com/question/37672218"
        parseDebugHTML(getHTML(url))
        url ="http://www.zhihu.com/question/38489486"
        parseDebugHTML(getHTML(url))
    else:
        load_user_agent()
        url = "https://www.zhihu.com/topics"
        html=getHTML(url)
        mt=getMainTopics(html)

        f=open("data.json",'a')
        print "total topics:"
        for t in mt:
            print "    "+t
        print "-----------------------------------------"

        file="topic/"+"3.html"
        ff=open(file,"r")
        html=ff.read()
        ff.close()

        st=getSubTopics(html,f)
        print "done"

        # for i,e in enumerate(mt):
        #     if i==0:
        #         continue
        #     if i>4:
        #         print "down"
        #         break
        #     # url = "https://www.zhihu.com/topics#"+e
        #     # print "processing "+url
        #     # html=getHTML(url)
        #     i+=1
        #     file="topic/"+str(i)+".html"
        #     ff=open(file,"r")
        #     html=ff.read()
        #     ff.close()
        #
        #     st=getSubTopics(html,f)
        #     print str(e)+"done"

        g=open("result",'w')
        g.write("succeed")
        g.close()

        f.close()




