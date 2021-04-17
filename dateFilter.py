import json
input_file=open('dateJsonOutput.json',encoding='utf8')
json_array = json.load(input_file)


for item in json_array:
    try:
        jsonstr=item['fileStr']
        jsonuuid=item['uuid']
        jsonmeta=item['metaUsed']
        jsonstkid=item['stockistId']
        jsonStrt=item['start_date']
        jsonEnd=item['end_date']
        if (jsonStrt!="2021-01-01 00:00:00") and (jsonStrt!="2020-12-25 00:00:00") and (jsonStrt!="2020-12-26 00:00:00") and (jsonStrt!="2020-12-27 00:00:00") and (jsonStrt!="2020-12-28 00:00:00") and (jsonStrt!="2020-12-29 00:00:00") and (jsonStrt!="2020-12-30 00:00:00") and (jsonStrt!="2020-12-31 00:00:00"):
            print(jsonStrt)
    except (KeyError, UnicodeEncodeError):
        pass