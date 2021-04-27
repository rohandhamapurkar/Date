import json #optional
import re
from datetime import date, datetime
import os   #optional
import sys #optional

def dateExt(text, fileuuid, meta, stkid):
    finalList=[]
    def dateComp(date1,date2,text,stkid,fileuuid):
        if date1>date2:
            start_date=date2
            end_date=date1
            dateList=[start_date, end_date]
            return dateList
        elif date2>date1:
            start_date=date1
            end_date=date2
            dateList=[start_date, end_date]
            return dateList
        else:
            start_date=date1
            dateList=[start_date]
            return dateList
    finalText=''
    text=text.lower()
    prefinalText=''
    for line in text.splitlines():
        if not "generated" in line and not "report date" in line and not "date/time" in line and not "run date" in line and not "print date" in line and not "valid upto" in line and not "data uploaded" in line and not "dl1:" in line and not "dl2:" in line and not "download" in line and not "d.no:" in line and not "licence no." in line and not "sh.no." in line: #licence no.   d.no:  SH.NO.
            prefinalText=prefinalText+"\n"+line

    finalText=re.sub(' +',' ',prefinalText)
    pattern1=r'\b(0?[1-9]|[12][0-9]|3[01])[- \/.](0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.](\d{4}|\d{2})\b' #remove w+ and match only motnths
    match = re.findall(pattern1,finalText)
    print(match,"m1")
    res=[]
    match1_2=[]
    if len(match)==2:
        tup1=match[0]   #1st tuple from match list
        tup2=match[1]   #2nd tuple from match list
        tup1='/'.join(tup1) #converting to string by "/"
        tup2='/'.join(tup2)
        for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
            try:
                date1 = datetime.strptime(tup1, frmt)
                date2 = datetime.strptime(tup2, frmt)
                remark="matching with 2dates and dd/mm/yyyy pattern"
                res=dateComp(date1,date2,text,stkid,fileuuid)
                #finalList.append(res)
            except ValueError:
                pass
    elif len(match)>2:
        lstdate=[]
        pattList_multiple=[]
        for i in range(len(match)):
            # locals()[f'tup{i}']=match[i]
            # locals()[f'tup{i}']='/'.join(locals()[f'tup{i}'])
            # print("date",locals()[f'tup{i}'])
            tup=match[i]
            tup='/'.join(tup)
            for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
                try:
                    date1 = datetime.strptime(tup, frmt)
                    lstdate.append(date1)
                except ValueError:
                    pass
        print(lstdate)
        for i in lstdate:
            print("debu")
            curyr=date.today().year
            if i.year==curyr or i.year==(curyr-1) or i.year==(curyr+1):
                pattList_multiple.append(i)
                print(pattList_multiple,"mul")
        if len(pattList_multiple)==2:
            res=dateComp(pattList_multiple[0],pattList_multiple[1],text,stkid,fileuuid)
        elif len(pattList_multiple)==1:
            finalList.append(pattList_multiple)
            print("final",finalList)
    elif len(match)==1:
        #again search for 01-jan
        #\n or \S
        tup1=match[0]
        tup1='/'.join(tup1)
        pattern1_2=r'\b(0?[1-9]|[12][0-9]|3[01])[- \/.,](jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[\s][- \/.,](\d{4}|\d{2})'
        match1_2 = re.findall(pattern1_2,finalText)
        print(match1_2)
        #31-jan -21
        if match1_2:
            tup2=match1_2[0]
            tup2='/'.join(tup2)
            for frmt in ("%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
                try:
                    date1 = datetime.strptime(tup1, frmt)
                    date2 = datetime.strptime(tup2, frmt)
                    remark="matching with 2dates and dd/mm/yyyy and dd/mm pattern"
                    res=dateComp(date1,date2,text,stkid,fileuuid)
                    #finalList.append(res)
                except ValueError:
                    pass
                    
        else:
            for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
                try:
                    date_one = datetime.strptime(tup1, frmt)
                    remark="matched with 1st pattern"
                    patt1List=[date_one]
                    finalList.append(patt1List)
                    print(finalList,"finalList append")
                except ValueError:
                   pass
    if len(match)==2:
        if len(res)>0:
            return res

    if len(match1_2)==1:
        if len(res)>0:
            return res
    if len(match)>2:
        if len(res)>0:
            return res

    #jan 01, 2021 to :- jan 31, 2021
    pattern5=r'\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.,](0?[1-9]|[12][0-9]|3[01])[- \/.,][- \/.,](\d{4}|\d{2})\b'
    match5 = re.findall(pattern5,finalText)
    print(match5,"m5")
    if len(match5) == 2:
        tup1=match5[0]   #1st tuple from match list
        tup2=match5[1]   #2nd tuple from match list
        tup1='/'.join(tup1) #converting to string by "/"
        tup2='/'.join(tup2)
        for frmt in ("%m/%d/%y","%m/%d/%Y","%B/%d/%Y","%b/%d/%Y","%B/%d/%y","%b/%d/%y"):
            try:
                date1 = datetime.strptime(tup1, frmt)
                date2 = datetime.strptime(tup2, frmt)
                res=dateComp(date1,date2,text,stkid,fileuuid)
                #finalList.append(res)
            except ValueError:
                pass
    elif len(match5)>2:
        lstdate=[]
        pattList_multiple=[]
        for i in range(len(match)):
            tup=match[i]
            tup='/'.join(tup)
            for frmt in ("%m/%d/%y","%m/%d/%Y","%B/%d/%Y","%b/%d/%Y","%B/%d/%y","%b/%d/%y"):
                try:
                    date1 = datetime.strptime(tup, frmt)
                    lstdate.append(date1)
                except ValueError:
                    pass
        for i in lstdate:
            curyr=date.today().year
            if i.year==curyr or i.year==(curyr-1) or i.year==(curyr+1):
                pattList_multiple.append(i)
                print(pattList_multiple,"mul")
        if len(pattList_multiple)==2:
            res=dateComp(pattList_multiple[0],pattList_multiple[1],text,stkid,fileuuid)
        elif len(pattList_multiple)==1:
            finalList.append(pattList_multiple)
    elif len(match5)==1:
        tup1=match5[0]   #1st tuple from match list
        tup1='/'.join(tup1)
        for frmt in ("%m/%d/%y","%m/%d/%Y","%B/%d/%Y","%b/%d/%Y","%B/%d/%y","%b/%d/%y"):
            try:
                date_one = datetime.strptime(tup1, frmt)
                patt5List=[date_one]
                finalList.append(patt5List)
            except ValueError:
                pass
    if len(match5)==2:
        if len(res)>0:
            return res

    if len(match5)>2:
        if len(res)>0:
            return res

    #matching with 2nd pattern
    #(?<!\S)
    pattern2=r"\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.,'](\d{4}|\d{2})\b"
    match2 = re.findall(pattern2,finalText)
    print(match2,"m2")
    if len(match2)==2:
        tup1=match2[0]
        tup2=match2[1]
        if tup1==tup2: #write code for not same dates
            lst1=list(tup1)
            lst2=list(tup2)
            if lst2[0]=="jan" or lst2[0]=="january" or lst2[0]=="mar" or lst2[0]=="march" or lst2[0]=="may" or lst2[0]=="aug" or lst2[0]=="august" or lst2[0]=="oct" or lst2[0]=="october" or lst2[0]=="dec" or lst2[0]=="december":
                endDay="31"
                
            elif lst2[0]=="feb" or lst2[0]=="february":
                endDay="28"

            elif lst2[0]=="apr" or lst2[0]=="april" or lst2[0]=="jun" or lst2[0]=="june" or lst2[0]=="jul" or lst2[0]=="july" or lst2[0]=="sept" or lst2[0]=="september" or lst2[0]=="nov" or lst2[0]=="november":
                endDay="30"        
            lst1.insert(0,"01") 
            lst2.insert(0,endDay)
            tup1=tuple(lst1)
            tup2=tuple(lst2)
            tup1='/'.join(tup1)
            tup2='/'.join(tup2)
            for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
                try:
                    date1 = datetime.strptime(tup1, frmt)
                    date2 = datetime.strptime(tup2, frmt)
                    remark="matching with 2dates and mm/yyyy pattern"
                    res=dateComp(date1,date2,text,stkid,fileuuid)
                except ValueError:
                    pass
        else:
            tup1='/'.join(tup1)
            tup2='/'.join(tup2)
            for frmt in ("%b/%y","%B/%y","%b/%Y","%B/%Y"):
                try:
                    date1 = datetime.strptime(tup1, frmt)
                    date2 = datetime.strptime(tup2, frmt)
                    remark="matching with 2nd pattern but 2 date"
                    res=dateComp(date1,date2,text,stkid,fileuuid)
                    #finalList.append(res)
                except ValueError:
                   pass
    elif len(match2)>2:
        lstdate=[]
        pattList_multiple=[]
        for i in range(len(match)):
            tup=match[i]
            tup='/'.join(tup)
            for frmt in ("%b/%y","%B/%y","%b/%Y","%B/%Y"):
                try:
                    date1 = datetime.strptime(tup, frmt)
                    lstdate.append(date1)
                except ValueError:
                    pass
        print(lstdate)
        for i in lstdate:
            print("debu")
            curyr=date.today().year
            if i.year==curyr or i.year==(curyr-1) or i.year==(curyr+1):
                pattList_multiple.append(i)
                print(pattList_multiple,"mul")
        if len(pattList_multiple)==2:
            res=dateComp(pattList_multiple[0],pattList_multiple[1],text,stkid,fileuuid)
        elif len(pattList_multiple)==1:
            finalList.append(pattList_multiple)
            print("final",finalList)

    elif len(match2)==1:
        tup1=match2[0]
        tup1='/'.join(tup1)
        for frmt in ("%b/%y","%B/%y","%b/%Y","%B/%Y"):
            try:
                date_one_only = datetime.strptime(tup1, frmt)
                remark="matching with 2nd pattern but 1 date"
                patt2List= [date_one_only]
                finalList.append(patt2List)
            except ValueError:
               pass
    if len(match2)==2:
        if len(res)>0:
            return res

    if len(match2)>2:
        if len(res)>0:
            return res

    #matching with 3rd pattern
    pattern3=r'\b(\d{4}|\d{2})[- \/.,](0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.,](0[1-9]|[12][0-9]|3[01])\b'
    match3 = re.findall(pattern3,finalText)
    print(match3,"m3")
    print(text)
    if len(match3)==2:
        tup1=match3[0]   #1st tuple from match list
        tup2=match3[1]   #2nd tuple from match list
        tup1='/'.join(tup1) #converting to string by "/"
        tup2='/'.join(tup2)
        for frmt in ("%y/%m/%d","%Y/%m/%d","%Y/%B/%d","%Y/%b/%d","%y/%B/%d","%y/%b/%d"):
            try:
                date1 = datetime.strptime(tup1, frmt)
                date2 = datetime.strptime(tup2, frmt)
                res=dateComp(date1,date2,text,stkid,fileuuid)
            except ValueError:
                pass
    elif len(match3)>2:
        lstdate=[]
        pattList_multiple=[]
        for i in range(len(match)):
            tup=match[i]
            tup='/'.join(tup)
            for frmt in ("%y/%m/%d","%Y/%m/%d","%Y/%B/%d","%Y/%b/%d","%y/%B/%d","%y/%b/%d"):
                try:
                    date1 = datetime.strptime(tup, frmt)
                    lstdate.append(date1)
                except ValueError:
                    pass
        print(lstdate)
        for i in lstdate:
            curyr=date.today().year
            if i.year==curyr or i.year==(curyr-1) or i.year==(curyr+1):
                pattList_multiple.append(i)
                print(pattList_multiple,"mul")
        if len(pattList_multiple)==2:
            res=dateComp(pattList_multiple[0],pattList_multiple[1],text,stkid,fileuuid)
        elif len(pattList_multiple)==1:
            finalList.append(pattList_multiple)

    elif len(match3)==1:
        tup1=match3[0]   #1st tuple from match list
        tup1='/'.join(tup1)
        for frmt in ("%y/%m/%d","%Y/%m/%d","%Y/%B/%d","%Y/%b/%d","%y/%B/%d","%y/%b/%d"):
            try:
                date_one_only = datetime.strptime(tup1, frmt)
                patt3List= [date_one_only]
                finalList.append(patt3List)
            except ValueError:
                pass

    if len(match3)==2:
        if len(res)>0:
            return res

    if len(match3)>2:
        if len(res)>0:
            return res

    #matching with 4th pattern
    pattern4=r"(?<!\S)(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(\d{4}|\d{2})\b"
    match4 = re.findall(pattern4,finalText)
    print(match4,"match4")
    if len(match4)==2:
        tup1=match4[0]
        tup2=match4[1]
        if tup1==tup2:
            lst1=list(tup1)
            lst2=list(tup2)
            if lst2[0]=="jan" or lst2[0]=="january" or lst2[0]=="mar" or lst2[0]=="march" or lst2[0]=="may" or lst2[0]=="aug" or lst2[0]=="august" or lst2[0]=="oct" or lst2[0]=="october" or lst2[0]=="dec" or lst2[0]=="december":
                endDay="31"
            if lst2[0]=="feb" or lst2[0]=="february":
                endDay="28"
            if lst2[0]=="apr" or lst2[0]=="april" or lst2[0]=="jun" or lst2[0]=="june" or lst2[0]=="jul" or lst2[0]=="july" or lst2[0]=="sept" or lst2[0]=="september" or lst2[0]=="nov" or lst2[0]=="november":
                endDay="30"        
            lst1.insert(0,"01") 
            lst2.insert(0,endDay)
            tup1=tuple(lst1)
            tup2=tuple(lst2)
            tup1='/'.join(tup1)
            tup2='/'.join(tup2)
            for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
                try:
                    date1 = datetime.strptime(tup1, frmt)
                    date2 = datetime.strptime(tup2, frmt)
                    remark="matching with 2dates and 4th pattern"
                    res=dateComp(date1,date2,text,stkid,fileuuid)
                    #finalList.append(res)
                except ValueError:
                    pass                
        else:
            tup1='/'.join(tup1)
            tup2='/'.join(tup2)
            for frmt in ("%b/%y","%B/%y","%b/%Y","%B/%Y"):
                try:
                    date1 = datetime.strptime(tup1, frmt)
                    date2 = datetime.strptime(tup2, frmt)
                    remark="matching with 2nd pattern but 2 date"
                    res=dateComp(date1,date2,text,stkid,fileuuid)
                    #finalList.append(res)
                except ValueError:
                   pass

    elif len(match4)>2:
        lstdate=[]
        pattList_multiple=[]
        for i in range(len(match)):
            tup=match[i]
            tup='/'.join(tup)
            for frmt in ("%b/%y","%B/%y","%b/%Y","%B/%Y"):
                try:
                    date1 = datetime.strptime(tup, frmt)
                    lstdate.append(date1)
                except ValueError:
                    pass
        for i in lstdate:
            curyr=date.today().year
            if i.year==curyr or i.year==(curyr-1) or i.year==(curyr+1):
                pattList_multiple.append(i)
        if len(pattList_multiple)==2:
            res=dateComp(pattList_multiple[0],pattList_multiple[1],text,stkid,fileuuid)
        elif len(pattList_multiple)==1:
            finalList.append(pattList_multiple)

    elif len(match4)==1:
        tup1=match4[0]
        tup1='/'.join(tup1)
        for frmt in ("%b/%y","%B/%y","%b/%Y","%B/%Y"):
            try:
                date_one_only = datetime.strptime(tup1, frmt)
                patt4List=[date_one_only]
                finalList.append(patt4List)
            except ValueError:
               pass
    if len(match4)==2:
        if len(res)>0:
            return res

    if len(match4)>2:
        if len(res)>0:
            return res

    if len(finalList)>0:
        #most=np.argmax([len(l) for l in finalList])
        return finalList[0]
#fileHeaderStringsv2
#wrongtry3
input_file=open('fileHeaderStringsMarch.json',encoding='utf8')
json_array = json.load(input_file)
try:
    for item in json_array:
        jsonstr=item['fileString']
        jsonuuid=item['uuid']
        jsonmeta=item['metaUsed']['$oid']
        jsonstkid=item['stockistId']
        jsonstr1=jsonstr.splitlines()[1:]
        jsonstr1="\n".join(x for x in jsonstr1)
        jsonstr2=jsonstr.splitlines()[:1]
        jsonstr2="\n".join(x for x in jsonstr2)  
        print("1",jsonstr)
        print("3",jsonstr2)
        print("2",jsonstr1)
        tp1=dateExt(jsonstr1,jsonuuid,jsonmeta,jsonstkid)
        if tp1:
            if len(tp1)==2:
                json_data={"fileStr":jsonstr, "uuid":jsonuuid,"metaUsed":jsonmeta,"start_date":str(tp1[0]),"end_date":str(tp1[1]),"stockistId":jsonstkid}
                with open("dateJsonOutput2.json", "a+") as outfile: 
                    json.dump(json_data, outfile, indent=4)
                    outfile.write(',\n')
            elif len(tp1)==1:
                print("tp1 len 1",tp1)
                json_data={"fileStr":jsonstr, "uuid":jsonuuid,"metaUsed":jsonmeta,"start_date":str(tp1[0]),"stockistId":jsonstkid}
                with open("dateJsonOutput2.json", "a+") as outfile: 
                    json.dump(json_data, outfile, indent=4)
                    outfile.write(',\n')
        else:
            tp2=dateExt(jsonstr2,jsonuuid,jsonmeta,jsonstkid)
            if tp2:
                if len(tp2)==2:
                    json_data={"fileStr":jsonstr, "uuid":jsonuuid,"metaUsed":jsonmeta,"start_date":str(tp2[0]),"end_date":str(tp2[1]),"stockistId":jsonstkid}
                    with open("dateJsonOutput2.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
                elif len(tp2)==1:
                    json_data={"fileStr":jsonstr, "uuid":jsonuuid,"metaUsed":jsonmeta,"start_date":str(tp2[0]),"stockistId":jsonstkid}
                    with open("dateJsonOutput2.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
            else:
                finalText_end=''
                jsonstr=jsonstr.replace("Date :\n","Date:")
                jsonstr=jsonstr.replace("Date:\n","Date:")
                for line in jsonstr.splitlines():
                    if not "Date:" in line and not "Date :" in line:
                        finalText_end=finalText_end+"\n"+line
                jsonstr3=finalText_end
                tp3=dateExt(jsonstr3,jsonuuid,jsonmeta,jsonstkid)
                if tp3:
                    if len(tp3)==2:
                        json_data={"fileStr":jsonstr, "uuid":jsonuuid,"metaUsed":jsonmeta,"start_date":str(tp3[0]),"end_date":str(tp3[1]),"stockistId":jsonstkid}
                        with open("dateJsonOutput2.json", "a+") as outfile: 
                            json.dump(json_data, outfile, indent=4)
                            outfile.write(',\n')
                else:
                    remark="no date found"
                    json_data={"fileStr":jsonstr, "uuid":jsonuuid,"metaUsed":jsonmeta,"stockistId":jsonstkid,"remark":remark}
                    with open("dateNotFound.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
except UnicodeEncodeError:
    pass
#todo date:\n to date:
#{"startDate":"data","endDate":"data2"},

#python3 script.py "str"