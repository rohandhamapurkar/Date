import json
import os
input_file=open('fileHeaderStringsMarch.json',encoding='utf8')
json_array = json.load(input_file)
for item in json_array:
    try:
        jsonstr=item['fileString']
        os.system(f"python3 dateNewApproachSysArgs.py {jsonstr}")
    except UnicodeEncodeError:
        pass