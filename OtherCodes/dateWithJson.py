import json
import re
from datetime import date, datetime

def dateExt(text, fileuuid, meta, stkid):
    pattern=r'\b(0?[1-9]|[12][0-9]|3[01])\b[^\w\d\r\n:](\w+)[^\w\d\r\n:](\d{4}|\d{2})'
    match = re.findall(pattern,text)
    print("length",len(match))
    print(match)
    if len(match)==2:
        tup1=match[0]   #1st tuple from match list
        tup2=match[1]   #2nd tuple from match list
        tup1='/'.join(tup1) #converting to string by "/"
        tup2='/'.join(tup2)
        for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
            try:
                date1 = datetime.strptime(tup1, frmt)
                date2 = datetime.strptime(tup2, frmt)
                print("matching with 1st pattern but 2dates")
                if date1>date2:
                    start_date=date2
                    end_date=date1
                    print("start date:",start_date)
                    print("end date:",end_date)
                    json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(start_date),"end_date":str(end_date),"stockistId":stkid}
                    with open("dateJsonOutput.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')

                if date2>date1:
                    start_date=date1
                    end_date=date2
                    print("start date:",start_date)
                    print("end date:",end_date)
                    json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(start_date),"end_date":str(end_date),"stockistId":stkid}
                    with open("dateJsonOutput.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
            except ValueError:
                pass
    if len(match)==1:
        tup1=match[0]
        tup1='/'.join(tup1)
        for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
            try:
                date_one = datetime.strptime(tup1, frmt)
                print("matching with 1st pattern but only 1 date")
                json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(date_one),"stockistId":stkid}
                with open("dateJsonOutput.json", "a+") as outfile: 
                    json.dump(json_data, outfile, indent=4)
                    outfile.write(',\n')
            except ValueError:
               pass

    if len(match)==0:
        try:                
            text=text.lower()
            pattern2=r"\b((0?[1-9]|1[0-2])|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b[^\w\d\r\n:](\d{4}|\d{2})"
            match = re.findall(pattern2,text)
            tup1=match[0]
            lst1=list(tup1)
            del lst1[1]
            print(lst1)
            tup1=tuple(lst1)
            tup1='/'.join(tup1)
            
            for frmt in ("%m/%y","%b/%y","%B/%y","%m/%Y","%b/%Y","%B/%Y"):
                try:
                    date_one_only = datetime.strptime(tup1, frmt)
                    print("matching with 2nd pattern")
                    json_data={"fileStr":text, "uuid":fileuuid,"metaUsed":meta,"start_date":str(date_one_only),"stockistId":stkid}
                    with open("dateJsonOutput.json", "a+") as outfile: 
                        json.dump(json_data, outfile, indent=4)
                        outfile.write(',\n')
                except ValueError:
                   pass
        except IndexError:
            pass
"""
import json

aList = [{"a":54, "b":87}, {"c":81, "d":63}, {"e":17, "f":39}]
jsonString = json.dumps(aList)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()"""

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
