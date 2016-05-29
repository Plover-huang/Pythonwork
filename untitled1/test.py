# -*- coding: utf-8 -*-
# import sys
#
#
# def rmstopword():
#     st=open('stopword','r')
#     cr=open('re_crawl','r')
#     re=open('rm_re',"w")
#     cr_content=cr.read()
#     a=4
#     st_line = st.readline().strip()
#     print st_line
#     print str(st_line)
#     while 1 :
#         #raw_input("press going on")
#         cr_content=cr_content.replace(st_line,'')
#         #print cr_content
#         #
#         st_line = st.readline().strip()
#         if not st_line:
#             break
#     re.write(cr_content)
#
#     st.close()
#     cr.close()
#     re.close()
#
#
# if __name__ == "__main__":
#     rmstopword()


#--------------------------------------------------------------

# from bs4 import BeautifulSoup
# import re,urllib2
#
# # f=open("test",'r')
# # html=f.read()
# # f.close()
# url="https://www.zhihu.com/topic/19567820/top-answers"
# html=urllib2.urlopen(url)
# soup=BeautifulSoup(html,"html.parser")
# kk=soup.find_all('a',href=re.compile('\?page=\d*?'))
# print kk[-2].text

#--------------------------------------------------------------


# 该代码爬取某个话题下的子话题
from bs4 import BeautifulSoup
import re,urllib2
url="https://www.zhihu.com/topics#艺术"
#url="https://www.zhihu.com/topics#游戏" #实际上爬取的是这个url的信息
html = urllib2.urlopen(url)
html = html.read()

soup = BeautifulSoup(html,"html.parser")
topics = soup.find_all('div',{"class":"item"})#获取子话题的标签
topics_even = soup.find_all('div',{"class":'item even'})#获取子话题的标签

topics+=topics_even #合并子话题

print "all sub topics are:"

for subTopic in topics:
    print subTopic.div.a.img.strong.text #打印子话题的内容




