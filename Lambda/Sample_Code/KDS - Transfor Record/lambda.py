import base64
import json

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        payload2 = transfor_data(payload)

def transfor_data(payload):
    data = json.loads(payload)
    data = data["log"]
    data = data.split()
    
    ls = []
    for i in data:
        ls.append(i)
    
    body = {
        "string": ls[0],
        "string": ls[1],
        "string": ls[2],
        "string": ls[3],
        "string": ls[4],
        "string": ls[5],
    }

    return json.dumps(body)