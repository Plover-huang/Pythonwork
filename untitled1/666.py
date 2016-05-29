for year in range(2015,2100):
    for num in range(1,10):
        if year%num==0:
            result = year/num
            sre = str(result)
            length=len(sre)
            flag=1
            finalstring=''
            for lt in range(0,length-1):
                if sre[lt]>sre[lt+1]:
                    flag=0
                    break
            if flag:
                for lt in range(0,length-1):
                    middlestring=(length-lt)*str(num)+" + "
                    finalstring+=int(sre[lt])*middlestring
                    a=int(sre[lt+1])-int(sre[lt])
                    l=list(sre)
                    sre.replace(sre[lt+1],str(a))
                    l[lt+1]=str(a)
                    sre=''.join(l)
                sre=str(result)
                a=int(sre[lt+1])-int(sre[lt])
                for k in range(0,a):
                    finalstring+=str(num)+" + "

                print str(year)+" = "+finalstring[:-2]
