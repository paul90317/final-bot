import os,json
with open('serviceAccountKey.json')as f:
    mjson=json.load(f)
    data=json.dumps(mjson)
    print(data)