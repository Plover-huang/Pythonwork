#-*- coding: UTF-8 -*-]
import json
import yaml
import ast
from BaikeExtract import Extract

def save_content(keyword,content):
    return None
def save_polysemant(keyword,polysemant):
    return None
def save_synonym(keyword, synonym):
    return None
def disambiguation(extObject,keyword,keywords_dict):
    content=extObject.getContent()
    target=0
    kk=content.find("<div class=\"main-content\">",0)
    page=content[kk:]
    for kw,na in keywords_dict.items():
        if kw!=keyword:
            target=target+str(page).count(kw)
    return target



def entitylinking(keywords_input):
    print keywords_input
    keywords_dict=ast.literal_eval(keywords_input)
    if str(type(keywords_dict))!='<type \'dict\'>':
        print "Error:the type of input is not dict"
        return None
    print keywords_dict
    # keywords = ["国奥","马晓旭", "殷家军", "中国人民解放军国防科学技术大学","沈阳", "国奥队", "雨水", "训练", "奥体中心", "外场", "球员"]
    # keywords = ["苹果","乔布斯","jobs"]
    # keywords = ["苹果","梨子"]#bad
    # keywords=["蜗牛","周杰伦"]
    keywords=[]
    keywordsURL = []
    keywords_search=[]
    print "-1(none) for entiry not found;\n0(Polysemants) for list page;\n1(Polysemant and content) for page with Polysemant;\n5(content and label and url not Polysemant maybe synonym) for unique page"
    for keyword,nature in keywords_dict.items():
        keywords.append(keyword)
        # keyword=keyword.encode("utf-8")
        print keyword+"\n=============================================================="
        bke = Extract(keyword,url=None)
        status=bke.getStatus()
        print "status:"+str(status)
        if status==-1:
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
                    print pl+"\t"+url+"<-- not exist"
                    continue
                target=disambiguation(content,keyword,keywords_dict)
                if target>=tempTarget:
                    tempTarget=target
                    tempUrl=url
                    tempPl=pl
                print pl+"\t"+url
            keywordsURL.append(tempUrl)
            keywords_search.append(tempPl)
        else:
            bkeContent=bke.getContent()
            print "content:\n"+bkeContent[:10]
            bkeSynonym=bke.getSynonym()
            if len(bkeSynonym)!=0:
                print "同义词:"+bkeSynonym
                keywords_search.append(bkeSynonym)
            else:
                keywords_search.append(keyword)
            bkeURL=bke.getURL()
            print "URL:"+bkeURL
            # bkeLable=bke.getLabel()
            # print "Lable: "+' '.join(bkeLable)
            keywordsURL.append(bkeURL)
    ll=len(keywords_dict)
    result=list()
    for i in range(ll):
        tempre=list()
        tempdict=dict()
        print keywords[i]+"\t"+keywords_search[i]+"\t"+keywordsURL[i]
        tempre.append(keywords_search[i])
        tempre.append(keywordsURL[i])
        tempdict[keywords[i]]=tempre
        result.append(tempdict)
    result_json=json.dumps(result)
    return result_json



input="{\"吹牛\":\"v\",\"也\":\"d\",\"要\":\"v\",\"按照\":\"p\",\"基本\":\"a\",\"法\":\"j\"}"
xx=entitylinking(input)
print xx


#
# for k,v in keywords,keywordsURL:
#     print k,v


'''
当识别到的实体没有歧义时直接返回链接，不做相关度计算
'''

    # #如果keyword在百科里对应多个实体，则需要消歧，在这之前按照要求需要把这些实体保存起来
    # #返回的类型是dict：k=Keyword_desc,v=url;e.g:训练_刘若英演唱歌曲:http://baike.baidu.com//subview/863276/11138816.htm
    # poly=bke.getPolysemant()
    # if len(poly)!=0:
    #     save_polysemant(keyword,poly)
    #     disambiguation(bke,keyword,keywords,poly)#在这个函数里设置bke正确的URL和页面
    # #消歧结束后，获得正确的实体以及实体的页面,把页面保存起来
    # content=bke.getContent()
    # if len(content):
    #     save_content(keyword,content)
    # syn=bke.getSynonym()
    # if len(syn)!=0:
    #     save_synonym(keyword,syn)





























