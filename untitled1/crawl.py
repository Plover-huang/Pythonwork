#-*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import urllib2 as u2
import json, re

i=0
base_link="http://www.zhihu.com"


def getHTML(url):
    # print "opening %s" % url
    html=u2.urlopen(url)
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

def parseTopicHTML(html):
    soup=BeautifulSoup(html,"html.parser")
    questions = soup.find_all('a',{"class":"question_link"})
    return questions

def parseQuestionHTML(html):
    soup=BeautifulSoup(html,"html.parser")
    content = soup.find_all("div",id="zh-question-detail")
    textarea = re.findall(r"<textarea class=\"content hidden\">",str(content[0]))
    if textarea:
        con = content[0].textarea.text
    else:
        con = content[0].text

    con = con.encode('UTF-8')
    con = str(con)
    # con = re.sub(r"[\u4e00-\u9fa5]","",con)
    con = re.sub(r'\w','',con)
    con = re.sub('[,./;\'\":?><=-_+-|)(*&^$#@!( )*?\t\n%/]','',con)
    return  con

def parseTopicsHTML(html):
    soup=BeautifulSoup(html,"html.parser")
    if i:
        print soup.prettify()
    else:
        topics = soup.find_all('div',{"class":"item"})
        topics_even = soup.find_all('div',{"class":'item even'})
        topics+=topics_even
        f=open("data.json",'w')
        data={}
        for topic in topics:
            topic_name = topic.div.a.img.strong.text #topic name
            url=base_link+topic.div.a["href"]
            questions = parseTopicHTML(getHTML(url))
            print "topic_name:"+topic_name
            data["topic"]=topic_name
            print "===================topic start==================="
            for question in questions: #question for each topic
                question_title = question.text #title
                print "question_title:"+question_title
                url = base_link+question["href"]
                question_desc = parseQuestionHTML(getHTML(url)).strip() #desc
                if question_desc=="":
                    question_desc="None"
                print "question_desc:"+question_desc
                print "--------------question--------------"
                data["title"]=question_title
                data["desc"]=question_desc
                json.dump(data,f)
                data={}

            print "===================topic end==================="

        f.close()



if __name__=="__main__":
    if i:
        url ="http://www.zhihu.com/question/37672218"
        parseDebugHTML(getHTML(url))
        url ="http://www.zhihu.com/question/38489486"
        parseDebugHTML(getHTML(url))
    else:
        f=open("topics.html",'r')
        html=f.read()
        f.close()
        parseTopicsHTML(html)