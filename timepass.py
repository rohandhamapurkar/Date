import re
from datetime import date, datetime
print("excecggg")
finalText="2/2/2021\n Stock and Sales Report\n 02 Feb, 2021 21:57:20\n Supplier:- KCCO From:- Jan 01, 2021 To :- Jan 31, 2021\n Mfg Name: ALKEM BERGEN ASTA"
finalText=finalText.lower()
pattern5=r'\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.,](0?[1-9]|[12][0-9]|3[01])[- \/.,][- \/.,](\d{4}|\d{2})\b'
match5 = re.findall(pattern5,finalText)
print("executing") 
if len(match5) == 2:
    print("match5")
    tup1=match5[0]   #1st tuple from match list
    tup2=match5[1]   #2nd tuple from match list
    tup1='/'.join(tup1) #converting to string by "/"
    tup2='/'.join(tup2)
    print(tup1)
    print(tup2)
    for frmt in ("%m/%d/%y","%m/%d/%Y","%B/%d/%Y","%b/%d/%Y","%B/%d/%y","%b/%d/%y"):
        try:
            date1 = datetime.strptime(tup1, frmt)
            date2 = datetime.strptime(tup2, frmt)
            remark="matching with 2dates and mm/dd/yyyy pattern"
            print(date1,"\n", date2,"\n", remark)
        except ValueError:
            pass
if len(match5)>0:
    print(len(match5))