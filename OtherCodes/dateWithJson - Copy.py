import json
import re
from datetime import date, datetime

def dateExt(text, fileuuid, meta, stkid):
    text=text.lower()
    finalText=''
    data=[]
    #date/time
    for line in text.splitlines():
        if not "report generated" in line and not "report date" in line:
            finalText=finalText+"\n"+line
    print(finalText)
    #* for optional
    #delimiter should be [-,/ and space]
    pattern1=r'\b(0?[1-9]|[12][0-9]|3[01])\b[^\w\d\r\n:](\w+)[^\w\d\r\n:](\d{4}|\d{2})' #remove w+ and match only motnths
    #pattern2=r"(?<!\S)(0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b[^\w\d\r\n:](\d{4}|\d{2})"
    match = re.findall(pattern1,finalText)

    print("data length",len(match))
    print(match)
    if len(match)==2:
        tup1=match[0]   #1st tuple from match list
        tup2=match[1]   #2nd tuple from match list
        print("debug",tup1)
        print("debug",tup2)
        tup1='/'.join(tup1) #converting to string by "/"
        tup2='/'.join(tup2)
        print("debug",tup1)
        print("debug",tup2)
        for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
            try:
                date1 = datetime.strptime(tup1, frmt)
                date2 = datetime.strptime(tup2, frmt)
                print(date1)
                print(date2)
                remark="matching with 2dates and dd/mm/yyyy pattern"
                if date1>date2:
                    start_date=date2
                    end_date=date1
                    print("start date:",start_date)
                    print("end date:",end_date)
                    json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(start_date),"end_date  ":str(end_date),"stockistId":stkid,"remark":remark}
                    with open("dateJsonOutput.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')

                if date2>date1:
                    start_date=date1
                    end_date=date2
                    print("start date:",start_date)
                    print("end date:",end_date)
                    json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(start_date),"end_date  ":str(end_date),"stockistId":stkid,"remark":remark}
                    with open("dateJsonOutput.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
                else:
                    start_date=date1
                    json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(start_date),"stockistId":stkid,"remark":remark}
                    with open("dateJsonOutput.json", "a+") as outfile:
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
            except ValueError as e:
                print("error", e)
    if len(data)==1:
        #again search for 01-jan
        tup1=data[0]
        tup1='/'.join(tup1)
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

    if len(data)==0:
        try:                
            pattern2=r"(?<!\S)(0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b[^\w\d\r\n:](\d{4}|\d{2})"
            match = re.findall(pattern2,finalText)
            tup1=match[0]
            print(tup1)
            tup1='/'.join(tup1)
            
            for frmt in ("%m/%y","%b/%y","%B/%y","%m/%Y","%b/%Y","%B/%Y"):
                try:
                    date_one_only = datetime.strptime(tup1, frmt)
                    remark="matching with mm/yy pattern"
                    json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(date_one_only),"stockistId":stkid,"remark":remark}
                    with open("dateJsonOutput.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
                except ValueError:
                   pass
        except IndexError:
            pass
        
        #for jan/21 jan/2021
        #(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(\d{4}|\d{2})
        #add another regex for yyyy/mm/dd
input_file = open ('stringwithmetas.json',encoding='utf8')
json_array = json.load(input_file)

try:
    for item in json_array:
        jsonstr=item['fileString']
        jsonuuid=item['uuid']
        jsonmeta=item['metaUsed']['$oid']
        jsonstkid=item['stockistId']
        dateExt(jsonstr,jsonuuid,jsonmeta,jsonstkid)
except UnicodeEncodeError:
    pass
