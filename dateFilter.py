import json
input_file=open('dateJsonOutput2.json',encoding='utf8')
json_array = json.load(input_file)

try:
    for item in json_array:
        jsonstr=item['fileStr']
        jsonuuid=item['uuid']
        jsonmeta=item['metaUsed']
        jsonstkid=item['stockistId']
        jsonStrt=item['start_date']
        jsonEnd=item['end_date']
        print(jsonstr,jsonuuid,jsonStrt,jsonEnd)
except (UnicodeEncodeError, KeyError):
    pass