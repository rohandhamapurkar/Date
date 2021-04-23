import json
input_file1=open('dateJsonOutputFinalAnalyzed.json',encoding='utf8')
json_array1 = json.load(input_file1)

input_file2=open('dateJsonOutput2.json',encoding='utf8')
json_array2 = json.load(input_file2)

def check(uuid,d1,d2):
    input_file2=open('dateJsonOutput2.json',encoding='utf8')
    json_array2 = json.load(input_file2)
    for item2 in json_array2:
        try:
            jsonuuid2=item2['uuid']
            jsondate2=item2['start_date']
            jsondate2end=item2['end_date']
            if uuid==jsonuuid2:
                if jsondate2==d1:
                    if jsondate2end==d2:
                        print(d1,jsondate2,uuid,"same")
                        break
                elif jsondate2end==d2:
                    print(d2,jsondate2end,uuid)
                else:
                    print(uuid, jsondate2,"not same")
            else:
                continue
        except (KeyError, UnicodeEncodeError, TypeError) as e:
            pass
for item in json_array1:
        try:
            jsonuuid=item['singleFile']['uuid']
            jsondate=item['singleFile']['start_date']
            jsondateend=item['singleFile']['end_date  ']
            check(jsonuuid,jsondate,jsondateend)
        except (KeyError, UnicodeEncodeError, TypeError) as e:
            pass