import re
from datetime import date, datetime
finalText="Reliance Drugs\n KALPETTA\n Stock & Sales Statement for the month of 01-01-20  02-02-21 03-03-26"
pattern1=r'\b(0?[1-9]|[12][0-9]|3[01])[- \/.](0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[- \/.](\d{4}|\d{2})\b' #remove w+ and match only motnths
match = re.findall(pattern1,finalText)
lstdate=[]
lstdate_list=[]
if len(match)>2:
    for i in range(len(match)):
        locals()[f'tup{i}']=match[i]
        locals()[f'tup{i}']='/'.join(locals()[f'tup{i}'])
        #print(locals()[f'tup{i}'])
        for frmt in ("%d/%m/%y","%d/%m/%Y","%d/%B/%Y","%d/%b/%Y","%d/%B/%y","%d/%b/%y"):
            try:
                date1 = datetime.strptime(locals()[f'tup{i}'], frmt)
                remark="matching with 2dates and dd/mm/yyyy pattern"
                #res=dateComp(date1,date2,remark,text,stkid,fileuuid)
                lstdate.append(date1)
            except ValueError:
                pass
    for i in lstdate:
        curyr=date.today().year
        if i.year==curyr or i.year==(curyr-1) or i.year==(curyr+1):
            lstdate_list.append(i)
    if len(lstdate_list)==2:
        res=dateComp(lstdate_list[0],lstdate_list[1],remark,text,stkid,fileuuid)