import json
input_file1=open('dateJsonOutputFinalAnalyzed.json',encoding='utf8')
json_array1 = json.load(input_file1)

input_file2=open('dateJsonOutput2.json',encoding='utf8')
json_array2 = json.load(input_file2)
'''
for key in crucial:
    if key in dishes:
        print dishes[key]'''
for item in json_array1:
    for item2 in json_array2:
        try:
            jsonuuid=item['singleFile']['uuid']
            jsondate=item['singleFile']['start_date']
            jsondate_end=item['singleFile']['end_date  ']
            jsonstr2=item2['fileStr']
            jsonuuid2=item2['uuid']
            jsondate2=item2['start_date']
            jsondate2_end=item2['end_date']
            if jsonuuid==jsonuuid2:
                if jsondate==jsondate2:
                    if jsondate_end==jsondate2_end:
                        print(jsondate,jsondate2,jsonuuid)
                    else:
                        print(jsondate,jsondate2,jsonuuid,"not same")
                else:
                    print(jsondate,jsondate2,jsonuuid,"not same")
        except (KeyError, UnicodeEncodeError, TypeError) as e:
            print(e)
            pass
