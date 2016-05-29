listnum=range(1,10)
for year in [9999,15120]:
    print str(year)
    ll=0
    for num in listnum:
        if year%num==0:
            result = year/num
            sre = str(result)
            length=len(sre)
            finalstring=''
            d1=list()
            m1=list()
            for lt in range(0,length):
                a='1'*(length-lt)
                d1.append(a)
                d=result/int(a)
                m1.append(d)
                result = result-d*int(a)
            for k in range(0,len(d1)):
                finalstring+=(str(int(d1[k])*num)+"+")*m1[k]
            print "    "+str(year)+"="+finalstring[:-1]
            if ll<len(finalstring):
                ll=len(finalstring)
    print "    "+"="*(ll+len(str(year)))


