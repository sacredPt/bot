import json
 

def read_json():
    f = open('config.json', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data