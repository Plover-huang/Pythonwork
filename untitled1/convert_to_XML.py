import re
import time
from os import listdir
from os.path import isfile,join

# #generate substitution
# replace={}
# with open("F:\convert_to_xml\changefile",'r') as oh:
#     doc=oh.readline()[:-1]
#     i=0
#     while doc:
#         doc1=oh.readline()[0:-1]
#         doc1=doc1.replace("\\n","\n")
#         replace[doc]=doc1
#         doc=oh.readline()[0:-1]
#     print replace
#
# # #convert to xml v1
# with open("F:\convert_to_xml\ohsumed","r") as oh:
#     doc=oh.readline()
#     count=0
#     content=""
#     while doc:
#         # print doc
#         key=doc[:2]
#         if key==".I":
#             # count+=1
#             no=doc[3:]
#         if replace.has_key(key):
#             value=replace[key]
#             doc=value+doc[3:]
#             if str(doc).__contains__("</DOC>"):
#                 doc=replace["</DOC>"]+doc[6:]
#         content=content+doc
#         # try:
#         doc=oh.readline()
#
#
#         key=doc[:2]
#         # time.sleep(2)
#         count+=1
#         if key==".I":
#             kk=content.split("\n")
#             if len(kk)==18:
#                 file=r'F:/convert_to_xml/ohsumed_result/doc%s' %no[:-1]
#                 print file,no[:-1]
#                 if(no[:-1]=="54720"):
#                     # time.sleep(1)
#                     pass
#                 wr=open(file,"w")
#                 wr.write(content)
#                 wr.close()
#             content=""

mypath=r"F:\convert_to_xml\ohsumed_result"
flist=[f for f in listdir(mypath) if isfile(join(mypath,f))]
flist.sort()
for f in flist:
    # fline=r"</AUTHOR></DOC>"
    # with open(join(mypath,f),"a") as fa:
    #     fa.write(fline)
    lbuffer=""
    with open(join(mypath,f),'r') as fr:
        lines=fr.readlines()
        # lbuffer=lines[1:]
        # print str(lbuffer)
        # time.sleep(2)
    with open(join(mypath,f),'w') as fw:
        for line in lines[1:]:
            fw.write(line)

    print join(mypath,f), f





