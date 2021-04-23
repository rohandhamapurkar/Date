import json
input_file1=open('dateJsonOutputFinalAnalyzed.json',encoding='utf8')
json_array1 = json.load(input_file1)

input_file2=open('dateJsonOutput2.json',encoding='utf8')
json_array2 = json.load(input_file2)

def check(uuid,d1):
    input_file2=open('dateJsonOutput2.json',encoding='utf8')
    json_array2 = json.load(input_file2)
    for item2 in json_array2:
        try:
            jsonuuid2=item2['uuid']
            jsondate2=item2['start_date']
            if uuid==jsonuuid2:
                if jsondate2==d1:
                    print(d1,jsondate2,uuid,"same")
                    break
                else:
                    print(d1,jsondate2,uuid,"not same")
            else:
                continue
        except (KeyError, UnicodeEncodeError, TypeError) as e:
            pass
for item in json_array1:
        try:
            jsonuuid=item['singleFile']['uuid']
            jsondate=item['singleFile']['start_date']
            check(jsonuuid,jsondate)
        except (KeyError, UnicodeEncodeError, TypeError) as e:
            pass