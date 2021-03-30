import json
import re
from datetime import date, datetime
import os
import sys
import calendar
def dateExt(text, fileuuid, meta, stkid):

    def dateComp(date1,date2,remark,text, stkid,fileuuid):
        print("uuid++++++++++",fileuuid)
        if date1>date2:
            start_date=date2
            end_date=date1
            json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(start_date),"end_date  ":str(end_date),"stockistId":stkid,"remark":remark}
            with open("dateJsonOutput.json", "a+") as outfile: 
                json.dump(json_data, outfile, indent=4)
                outfile.write(',\n')
                print("writing")
        if date2>date1:
            start_date=date1
            end_date=date2
            json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(start_date),"end_date  ":str(end_date),"stockistId":stkid,"remark":remark}
            with open("dateJsonOutput.json", "a+") as outfile: 
                json.dump(json_data, outfile, indent=4)
                outfile.write(',\n')
                print("writing")
        else:
            start_date=date1
            json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(start_date),"stockistId":stkid,"remark":remark}
            with open("dateJsonOutput.json", "a+") as outfile:
                json.dump(json_data, outfile, indent=4)
                outfile.write(',\n')
                print("writing")
    '''
    def dateGenerator(date_one,remark):
        #25/dec/2020
        strt_days=[1,2,3,4,5,6,7]
        end_days=[25,26,27,28,29,30,31]
        date_one_day=date_one.day
        date_one_month=date_one.month
        date_one_year=date_one.year
        _,last_day= calendar.monthrange(date_one_year, date_one_month)
        if date_one_day in strt_days:
            date_two=str(last_day)+"/"+str(date_one_month)+"/"+str(date_one_year)
            date_two = datetime.strptime(date_two, "%d/%m/%Y")

        if date_one_day in end_days:
            date_two="01"+"/"+str(date_one_month)+"/"+str(date_one_year)
            date_two = datetime.strptime(date_two, "%d/%m/%Y")
        dateComp(date_one, date_two, remark)'''

    text=text.lower()
    prefinalText=''
    text=text.splitlines()[1:]
    text="\n".join(x for x in text)
    for line in text.splitlines():
        if not "generated" in line and not "report date" in line and not "date/time" in line and not "run date" in line and not "print date" in line and not "valid upto" in line and not "data uploaded" in line:
            prefinalText=prefinalText+"\n"+line
    finalText=re.sub(' +',' ',prefinalText) #multuple spaces to one space

    pattern1=r'(to)?(0?[1-9]|[12][0-9]|3[01])[- \/.,](0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.,](\d{4}|\d{2})(to)?' 
    match = re.findall(pattern1,finalText)
    if len(match)==2:
        tup1=match[0]   #1st tuple from match list
        tup2=match[1]   #2nd tuple from match list
        # tup1='/'.join(tup1) #converting to string by "/"
        # tup2='/'.join(tup2)
        lst1=list(tup1)
        lst2=list(tup2)
        lst1.pop(4)
        lst1.pop(0)
        lst2.pop(4)
        lst2.pop(0)
        tup1=tuple(lst1)
        tup1='/'.join(tup1)
        tup2=tuple(lst2)
        tup2='/'.join(tup2)

        for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
            try:
                date_1 = datetime.strptime(tup1, frmt)
                date_2 = datetime.strptime(tup2, frmt)
                rmrk="matching with 2dates and dd/mm/yyyy pattern"
                dateComp(date_1,date_2,rmrk,text,stkid,fileuuid)
            except ValueError:
                pass

    if len(match)==1:
        tup1=match[0]
        tup1='/'.join(tup1)
        pattern1_2=r'(0?[1-9]|[12][0-9]|3[01])[- \/.,](jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[\s][- \/.,](\d{4}|\d{2})'
        match1_2 = re.findall(pattern1_2,finalText)
        if match1_2:
            tup2=match1_2[0]
            tup2='/'.join(tup2)
            for frmt in ("%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
                try:
                    date_1 = datetime.strptime(tup1, frmt)
                    date_2 = datetime.strptime(tup2, frmt)
                    rmrk="matching with 2dates and dd/mm/yyyy and dd/mm pattern"
                    dateComp(date_1,date_2,rmrk,text,stkid,fileuuid)
                except ValueError:
                   pass
            
            
        else:
            for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
                try:
                    date_one = datetime.strptime(tup1, frmt)
                    remark="matching with only 1 date and dd/mm/yyyy pattern"
                    json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(date_one),"stockistId":stkid,"remark":remark}
                    with open("dateJsonOutput.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
                except ValueError:
                   pass

    if len(match)>0:
        return
        

    #matching with 2nd pattern
    pattern2=r"(?<!\S)(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.,](\d{4}|\d{2})"
    match2 = re.findall(pattern2,finalText)
    if len(match2)==2:
        tup1=match2[0]
        tup2=match2[1]
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
                    date_1 = datetime.strptime(tup1, frmt)
                    date_2 = datetime.strptime(tup2, frmt)
                    rmrk="matching with 2dates and mm/yyyy pattern"
                    dateComp(date_1,date_2,rmrk,text,stkid,fileuuid)
                except ValueError:
                    pass
    if len(match2)==1:
        tup1=match2[0]
        tup1='/'.join(tup1)
        print("matching with 2nd pattern 1 date")
        for frmt in ("%b/%y","%B/%y","%b/%Y","%B/%Y"):
            try:
                date_one_only = datetime.strptime(tup1, frmt)
                remark="matching with 2nd pattern but 1 date"
                json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(date_one_only),"stockistId":stkid,"remark":remark}
                with open("dateJsonOutput.json", "a+") as outfile: 
                    json.dump(json_data, outfile, indent=4)
                    outfile.write(',\n')
            except ValueError:
               pass

    if len(match2)>0:
        return

    #matching with 3rd pattern
    pattern3=r'(\d{4}|\d{2})[- \/.,]\b(0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.,](0[1-9]|[12][0-9]|3[01])'
    match3 = re.findall(pattern3,finalText)
    if len(match3)==2:
        tup1=match3[0]   #1st tuple from match list
        tup2=match3[1]   #2nd tuple from match list
        tup1='/'.join(tup1) #converting to string by "/"
        tup2='/'.join(tup2)
        for frmt in ("%y/%m/%d","%Y/%m/%d","%Y/%B/%d","%Y/%b/%d","%y/%B/%d","%y/%b/%d"):
            try:
                date_1 = datetime.strptime(tup1, frmt)
                date_2 = datetime.strptime(tup2, frmt)
                rmrk="yyyy/mm/dd pattern and matching with 2dates"
                dateComp(date_1,date_2,rmrk,text,stkid,fileuuid)
            except ValueError:
                pass
    if len(match3)>0:
        return
        
    #matching with 4th pattern
    pattern4=r"(?<!\S)(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(\d{4}|\d{2})"
    match4 = re.findall(pattern4,finalText)
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
                    date_1 = datetime.strptime(tup1, frmt)
                    date_2 = datetime.strptime(tup2, frmt)
                    rmrk="matching with 2dates and 4th pattern"
                    dateComp(date_1,date_2,rmrk,text,stkid,fileuuid)
                except ValueError:
                    pass
    if len(match4)==1:        
        tup1=match4[0]
        print("match tup1 4th", tup1)
        tup1='/'.join(tup1)
        
        print("matching with 4th pattern 1 date")
        for frmt in ("%b/%y","%B/%y","%b/%Y","%B/%Y"):
            try:
                date_one_only = datetime.strptime(tup1, frmt)
                remark="matching with 4th pattern but 1 date"
                json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(date_one_only),"stockistId":stkid,"remark":remark}
                with open("dateJsonOutput.json", "a+") as outfile: 
                    json.dump(json_data, outfile, indent=4)
                    outfile.write(',\n')
            except ValueError:
               pass
    if len(match4)>0:
        return
    else:
        remark="no date found"
        json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"stockistId":stkid,"remark":remark}
        with open("dateJsonOutput.json", "a+") as outfile: 
            json.dump(json_data, outfile, indent=4)
            outfile.write(',\n')
    #jan 01, 2021 to :- jan 31, 2021
input_file=open('wrongtry.json',encoding='utf8')
json_array = json.load(input_file)
try:
    for item in json_array:
        jsonstr=item['fileString']
        jsonuuid=item['uuid']
        jsonmeta=item['metaUsed']['$oid']
        jsonstkid=item['stockistId']
        dateExt(jsonstr,jsonuuid,jsonmeta,jsonstkid)
except UnicodeEncodeError:
    print("unicode error")
